"""Detector for Duplicated Code smell."""

import ast
from difflib import SequenceMatcher
from .base_detector import BaseDetector


class DuplicatedCodeDetector(BaseDetector):
    """Detects duplicated code blocks."""
    
    def get_name(self):
        return "DuplicatedCode"
    
    def detect(self, ast_tree, source_code, filename):
        """Detect duplicated code in the source."""
        smells = []
        min_lines = self.config.get('min_lines', 5)
        similarity_threshold = self.config.get('similarity_threshold', 0.85)
        
        # Extract all methods/functions
        methods = []
        for node in ast.walk(ast_tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                    lines = source_code.split('\n')[node.lineno - 1:node.end_lineno]
                    method_code = '\n'.join(lines)
                    methods.append({
                        'name': node.name,
                        'start': node.lineno,
                        'end': node.end_lineno,
                        'code': method_code,
                        'lines': lines
                    })
        
        # Compare methods for similarity
        reported_pairs = set()
        for i, method1 in enumerate(methods):
            for j, method2 in enumerate(methods):
                if i >= j:
                    continue
                
                # Skip if already reported
                pair_key = tuple(sorted([method1['name'], method2['name']]))
                if pair_key in reported_pairs:
                    continue
                
                # Calculate similarity
                similarity = self._calculate_similarity(method1['code'], method2['code'])
                
                if similarity >= similarity_threshold:
                    reported_pairs.add(pair_key)
                    description = (f"Duplicated code between methods '{method1['name']}' "
                                 f"(lines {method1['start']}-{method1['end']}) and "
                                 f"'{method2['name']}' (lines {method2['start']}-{method2['end']}). "
                                 f"Similarity: {similarity:.2%}")
                    smells.append(self.format_smell(
                        filename,
                        method1['start'],
                        method2['end'],
                        description,
                        severity='medium'
                    ))
        
        # Also check for duplicated blocks within the same method
        for method in methods:
            if len(method['lines']) >= min_lines * 2:
                blocks = self._extract_blocks(method['lines'], min_lines)
                duplicates = self._find_duplicate_blocks(blocks, similarity_threshold)
                
                for dup in duplicates:
                    description = (f"Duplicated code block within method '{method['name']}'. "
                                 f"Similarity: {dup['similarity']:.2%}")
                    smells.append(self.format_smell(
                        filename,
                        method['start'] + dup['block1_start'],
                        method['start'] + dup['block2_end'],
                        description,
                        severity='low'
                    ))
        
        return smells
    
    def _calculate_similarity(self, text1, text2):
        """Calculate similarity ratio between two text blocks."""
        # Normalize whitespace for comparison
        normalized1 = ' '.join(text1.split())
        normalized2 = ' '.join(text2.split())
        return SequenceMatcher(None, normalized1, normalized2).ratio()
    
    def _extract_blocks(self, lines, min_size):
        """Extract code blocks of minimum size from lines."""
        blocks = []
        for i in range(len(lines) - min_size + 1):
            block = lines[i:i + min_size]
            blocks.append({
                'start': i,
                'end': i + min_size - 1,
                'code': '\n'.join(block)
            })
        return blocks
    
    def _find_duplicate_blocks(self, blocks, threshold):
        """Find duplicate blocks within a method."""
        duplicates = []
        for i, block1 in enumerate(blocks):
            for j, block2 in enumerate(blocks):
                if i >= j:
                    continue
                
                similarity = self._calculate_similarity(block1['code'], block2['code'])
                if similarity >= threshold:
                    duplicates.append({
                        'block1_start': block1['start'],
                        'block1_end': block1['end'],
                        'block2_start': block2['start'],
                        'block2_end': block2['end'],
                        'similarity': similarity
                    })
        
        return duplicates


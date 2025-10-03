"""Detector for Magic Numbers code smell."""

import ast
from .base_detector import BaseDetector


class MagicNumbersDetector(BaseDetector):
    """Detects magic numbers (hard-coded numeric literals)."""
    
    def get_name(self):
        return "MagicNumbers"
    
    def detect(self, ast_tree, source_code, filename):
        """Detect magic numbers in the code."""
        smells = []
        allowed_numbers = set(self.config.get('allowed_numbers', [0, 1, -1, 2]))
        
        # Track magic numbers by line to avoid duplicates
        magic_by_line = {}
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.Num):
                # Check if it's a magic number
                value = node.n
                
                # Skip allowed numbers and floats that are close to allowed integers
                if value not in allowed_numbers:
                    if hasattr(node, 'lineno'):
                        line = node.lineno
                        if line not in magic_by_line:
                            magic_by_line[line] = []
                        magic_by_line[line].append(value)
            
            # Also check ast.Constant for Python 3.8+
            elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                value = node.value
                
                if value not in allowed_numbers:
                    if hasattr(node, 'lineno'):
                        line = node.lineno
                        if line not in magic_by_line:
                            magic_by_line[line] = []
                        if value not in magic_by_line[line]:
                            magic_by_line[line].append(value)
        
        # Create smell reports for each line with magic numbers
        for line, values in magic_by_line.items():
            unique_values = list(set(values))
            description = (f"Magic number(s) found: {unique_values}. "
                         f"Consider using named constants for better readability")
            smells.append(self.format_smell(
                filename,
                line,
                line,
                description,
                severity='low'
            ))
        
        return smells


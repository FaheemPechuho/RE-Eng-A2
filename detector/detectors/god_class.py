"""Detector for God Class (Blob) code smell."""

import ast
from .base_detector import BaseDetector


class GodClassDetector(BaseDetector):
    """Detects classes that do too many things (God Class/Blob)."""
    
    def get_name(self):
        return "GodClass"
    
    def detect(self, ast_tree, source_code, filename):
        """Detect God Classes in the code."""
        smells = []
        method_threshold = self.config.get('method_threshold', 10)
        line_threshold = self.config.get('line_threshold', 150)
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.ClassDef):
                # Count methods in the class
                methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                method_count = len(methods)
                
                # Calculate lines in the class
                if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                    class_lines = node.end_lineno - node.lineno + 1
                    
                    # Check if it's a God Class
                    is_god_class = (method_count >= method_threshold or class_lines >= line_threshold)
                    
                    if is_god_class:
                        reasons = []
                        if method_count >= method_threshold:
                            reasons.append(f"{method_count} methods (threshold: {method_threshold})")
                        if class_lines >= line_threshold:
                            reasons.append(f"{class_lines} lines (threshold: {line_threshold})")
                        
                        description = (f"Class '{node.name}' is a God Class with "
                                     f"{', '.join(reasons)}")
                        smells.append(self.format_smell(
                            filename,
                            node.lineno,
                            node.end_lineno,
                            description,
                            severity='high'
                        ))
        
        return smells


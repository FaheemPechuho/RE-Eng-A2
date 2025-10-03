"""Detector for Long Method code smell."""

import ast
from .base_detector import BaseDetector


class LongMethodDetector(BaseDetector):
    """Detects methods that are too long."""
    
    def get_name(self):
        return "LongMethod"
    
    def detect(self, ast_tree, source_code, filename):
        """Detect long methods in the code."""
        smells = []
        threshold = self.config.get('threshold', 30)
        
        for node in ast.walk(ast_tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Calculate the number of lines in the method
                if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                    method_lines = node.end_lineno - node.lineno + 1
                    
                    if method_lines > threshold:
                        description = (f"Method '{node.name}' has {method_lines} lines, "
                                     f"exceeding threshold of {threshold} lines")
                        smells.append(self.format_smell(
                            filename,
                            node.lineno,
                            node.end_lineno,
                            description,
                            severity='high' if method_lines > threshold * 1.5 else 'medium'
                        ))
        
        return smells


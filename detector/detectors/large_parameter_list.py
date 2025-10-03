"""Detector for Large Parameter List code smell."""

import ast
from .base_detector import BaseDetector


class LargeParameterListDetector(BaseDetector):
    """Detects methods with too many parameters."""
    
    def get_name(self):
        return "LargeParameterList"
    
    def detect(self, ast_tree, source_code, filename):
        """Detect methods with large parameter lists."""
        smells = []
        threshold = self.config.get('threshold', 5)
        
        for node in ast.walk(ast_tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Count parameters (excluding self/cls)
                params = node.args.args
                param_count = len(params)
                
                # Exclude 'self' or 'cls' for methods
                if param_count > 0 and params[0].arg in ['self', 'cls']:
                    param_count -= 1
                
                if param_count >= threshold:
                    param_names = [arg.arg for arg in params]
                    description = (f"Method '{node.name}' has {param_count} parameters "
                                 f"(threshold: {threshold}). Parameters: {', '.join(param_names)}")
                    smells.append(self.format_smell(
                        filename,
                        node.lineno,
                        node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
                        description,
                        severity='high' if param_count >= threshold + 2 else 'medium'
                    ))
        
        return smells


"""Detector for Feature Envy code smell."""

import ast
from collections import defaultdict
from .base_detector import BaseDetector


class FeatureEnvyDetector(BaseDetector):
    """Detects methods that access other classes' data more than their own."""
    
    def get_name(self):
        return "FeatureEnvy"
    
    def detect(self, ast_tree, source_code, filename):
        """Detect feature envy in methods."""
        smells = []
        external_call_ratio = self.config.get('external_call_ratio', 0.6)
        min_external_calls = self.config.get('min_external_calls', 3)
        
        # Build a map of classes and their methods
        class_map = {}
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.ClassDef):
                class_map[node.name] = node
        
        # Analyze each method
        for class_name, class_node in class_map.items():
            for node in class_node.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Skip __init__ and other special methods
                    if node.name.startswith('__'):
                        continue
                    
                    # Count attribute accesses
                    accesses = self._count_attribute_accesses(node)
                    
                    total_calls = sum(accesses.values())
                    if total_calls == 0:
                        continue
                    
                    # Count external accesses (not self)
                    external_calls = sum(count for var, count in accesses.items() if var != 'self')
                    
                    if external_calls >= min_external_calls:
                        ratio = external_calls / total_calls
                        
                        if ratio >= external_call_ratio:
                            main_envied = max(
                                ((var, count) for var, count in accesses.items() if var != 'self'),
                                key=lambda x: x[1],
                                default=(None, 0)
                            )
                            
                            description = (f"Method '{node.name}' in class '{class_name}' "
                                         f"shows feature envy. {external_calls}/{total_calls} "
                                         f"({ratio:.1%}) attribute accesses are to external objects. "
                                         f"Most accessed: '{main_envied[0]}' ({main_envied[1]} times)")
                            smells.append(self.format_smell(
                                filename,
                                node.lineno,
                                node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
                                description,
                                severity='medium'
                            ))
        
        return smells
    
    def _count_attribute_accesses(self, method_node):
        """Count attribute accesses in a method."""
        accesses = defaultdict(int)
        
        for node in ast.walk(method_node):
            if isinstance(node, ast.Attribute):
                # Get the base object being accessed
                if isinstance(node.value, ast.Name):
                    var_name = node.value.id
                    accesses[var_name] += 1
                elif isinstance(node.value, ast.Call):
                    # Method chaining or call results
                    if isinstance(node.value.func, ast.Name):
                        var_name = node.value.func.id
                        accesses[var_name] += 1
            
            # Also count method calls on objects
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        var_name = node.func.value.id
                        accesses[var_name] += 1
        
        return dict(accesses)


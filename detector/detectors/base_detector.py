"""Base class for all code smell detectors."""

from abc import ABC, abstractmethod


class BaseDetector(ABC):
    """Abstract base class for code smell detectors."""
    
    def __init__(self, config):
        """Initialize detector with configuration."""
        self.config = config
    
    @abstractmethod
    def detect(self, ast_tree, source_code, filename):
        """
        Detect code smells in the given AST and source code.
        
        Args:
            ast_tree: AST tree of the source code
            source_code: Raw source code as string
            filename: Name of the file being analyzed
        
        Returns:
            List of detected smell instances
        """
        pass
    
    @abstractmethod
    def get_name(self):
        """Get the name of this detector."""
        pass
    
    def format_smell(self, filename, line_start, line_end, description, severity='medium'):
        """
        Format a detected smell into a standard structure.
        
        Args:
            filename: Name of the file
            line_start: Starting line number
            line_end: Ending line number
            description: Description of the smell
            severity: Severity level (low, medium, high)
        
        Returns:
            Dictionary containing smell information
        """
        return {
            'smell_type': self.get_name(),
            'file': filename,
            'line_start': line_start,
            'line_end': line_end,
            'description': description,
            'severity': severity
        }


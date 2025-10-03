#!/usr/bin/env python3
"""
Code Smell Detector - Main Entry Point
Detects common code smells in Python source code.
"""

import ast
import argparse
import sys
import os
import yaml
from pathlib import Path
from datetime import datetime

from detectors import (
    LongMethodDetector,
    GodClassDetector,
    DuplicatedCodeDetector,
    LargeParameterListDetector,
    MagicNumbersDetector,
    FeatureEnvyDetector
)


class CodeSmellDetector:
    """Main detector class that coordinates all smell detectors."""
    
    DETECTOR_CLASSES = {
        'LongMethod': LongMethodDetector,
        'GodClass': GodClassDetector,
        'DuplicatedCode': DuplicatedCodeDetector,
        'LargeParameterList': LargeParameterListDetector,
        'MagicNumbers': MagicNumbersDetector,
        'FeatureEnvy': FeatureEnvyDetector
    }
    
    def __init__(self, config_path='config.yaml'):
        """Initialize the detector with configuration."""
        self.config = self._load_config(config_path)
        self.detectors = {}
        self.active_detectors = []
    
    def _load_config(self, config_path):
        """Load configuration from YAML file."""
        if not os.path.exists(config_path):
            print(f"Warning: Config file '{config_path}' not found. Using defaults.")
            return self._get_default_config()
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
            return self._get_default_config()
    
    def _get_default_config(self):
        """Get default configuration."""
        return {
            'detectors': {
                'LongMethod': {'enabled': True, 'threshold': 30},
                'GodClass': {'enabled': True, 'method_threshold': 10, 'line_threshold': 150},
                'DuplicatedCode': {'enabled': True, 'min_lines': 5, 'similarity_threshold': 0.85},
                'LargeParameterList': {'enabled': True, 'threshold': 5},
                'MagicNumbers': {'enabled': True, 'allowed_numbers': [0, 1, -1, 2]},
                'FeatureEnvy': {'enabled': True, 'external_call_ratio': 0.6, 'min_external_calls': 3}
            }
        }
    
    def initialize_detectors(self, only=None, exclude=None):
        """
        Initialize detectors based on config and CLI arguments.
        
        Args:
            only: List of detector names to run exclusively
            exclude: List of detector names to exclude
        """
        detector_configs = self.config.get('detectors', {})
        
        for detector_name, detector_class in self.DETECTOR_CLASSES.items():
            # Get detector config
            detector_config = detector_configs.get(detector_name, {})
            
            # Determine if this detector should be active
            should_activate = False
            
            if only:
                # CLI --only flag overrides everything
                should_activate = detector_name in only
            elif exclude:
                # CLI --exclude flag overrides config
                enabled_in_config = detector_config.get('enabled', True)
                should_activate = enabled_in_config and detector_name not in exclude
            else:
                # Use config file setting
                should_activate = detector_config.get('enabled', True)
            
            # Create detector instance
            self.detectors[detector_name] = detector_class(detector_config)
            
            if should_activate:
                self.active_detectors.append(detector_name)
    
    def analyze_file(self, filepath):
        """
        Analyze a single Python file for code smells.
        
        Args:
            filepath: Path to the Python file
        
        Returns:
            Dictionary containing analysis results
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Parse the source code into AST
            try:
                ast_tree = ast.parse(source_code, filename=filepath)
            except SyntaxError as e:
                return {
                    'file': filepath,
                    'error': f"Syntax error: {e}",
                    'smells': []
                }
            
            # Run active detectors
            all_smells = []
            for detector_name in self.active_detectors:
                detector = self.detectors[detector_name]
                smells = detector.detect(ast_tree, source_code, filepath)
                all_smells.extend(smells)
            
            return {
                'file': filepath,
                'smells': all_smells,
                'smell_count': len(all_smells)
            }
        
        except Exception as e:
            return {
                'file': filepath,
                'error': str(e),
                'smells': []
            }
    
    def analyze_directory(self, directory):
        """
        Analyze all Python files in a directory.
        
        Args:
            directory: Path to directory
        
        Returns:
            List of analysis results for each file
        """
        results = []
        path = Path(directory)
        
        for py_file in path.rglob('*.py'):
            result = self.analyze_file(str(py_file))
            results.append(result)
        
        return results
    
    def generate_report(self, results, output_format='text'):
        """
        Generate a report from analysis results.
        
        Args:
            results: Analysis results
            output_format: Format of output ('text' or 'json')
        
        Returns:
            Formatted report string
        """
        if output_format == 'json':
            import json
            return json.dumps({
                'timestamp': datetime.now().isoformat(),
                'active_detectors': self.active_detectors,
                'results': results
            }, indent=2)
        
        # Text format
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("CODE SMELL DETECTION REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Active Detectors: {', '.join(self.active_detectors)}")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        total_smells = 0
        
        for result in results:
            filepath = result['file']
            
            if 'error' in result:
                report_lines.append(f"File: {filepath}")
                report_lines.append(f"  ERROR: {result['error']}")
                report_lines.append("")
                continue
            
            smells = result['smells']
            total_smells += len(smells)
            
            report_lines.append(f"File: {filepath}")
            report_lines.append(f"  Total Smells: {len(smells)}")
            
            if smells:
                report_lines.append("")
                # Group by smell type
                by_type = {}
                for smell in smells:
                    smell_type = smell['smell_type']
                    if smell_type not in by_type:
                        by_type[smell_type] = []
                    by_type[smell_type].append(smell)
                
                for smell_type, smell_list in by_type.items():
                    report_lines.append(f"  {smell_type} ({len(smell_list)} instance(s)):")
                    for smell in smell_list:
                        line_info = f"lines {smell['line_start']}-{smell['line_end']}"
                        if smell['line_start'] == smell['line_end']:
                            line_info = f"line {smell['line_start']}"
                        report_lines.append(f"    - {line_info} [{smell['severity']}]")
                        report_lines.append(f"      {smell['description']}")
                    report_lines.append("")
            
            report_lines.append("-" * 80)
            report_lines.append("")
        
        report_lines.append("=" * 80)
        report_lines.append(f"SUMMARY: {total_smells} total code smell(s) detected")
        report_lines.append("=" * 80)
        
        return '\n'.join(report_lines)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Detect code smells in Python source code',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single file with all enabled detectors
  python main.py mycode.py
  
  # Analyze a directory
  python main.py src/
  
  # Run only specific detectors
  python main.py --only LongMethod,MagicNumbers mycode.py
  
  # Run all except specific detectors
  python main.py --exclude DuplicatedCode mycode.py
  
  # Specify custom config file
  python main.py --config custom_config.yaml mycode.py
  
  # Output as JSON
  python main.py --format json mycode.py
        """
    )
    
    parser.add_argument(
        'path',
        help='Path to Python file or directory to analyze'
    )
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--only',
        help='Run only specified detectors (comma-separated, e.g., LongMethod,GodClass)'
    )
    
    parser.add_argument(
        '--exclude',
        help='Exclude specified detectors (comma-separated)'
    )
    
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Parse only/exclude arguments
    only_detectors = None
    exclude_detectors = None
    
    if args.only:
        only_detectors = [d.strip() for d in args.only.split(',')]
    if args.exclude:
        exclude_detectors = [d.strip() for d in args.exclude.split(',')]
    
    # Initialize detector
    detector = CodeSmellDetector(args.config)
    detector.initialize_detectors(only=only_detectors, exclude=exclude_detectors)
    
    if not detector.active_detectors:
        print("Error: No detectors are active. Check your configuration.")
        sys.exit(1)
    
    # Analyze path
    if os.path.isfile(args.path):
        results = [detector.analyze_file(args.path)]
    elif os.path.isdir(args.path):
        results = detector.analyze_directory(args.path)
    else:
        print(f"Error: Path '{args.path}' does not exist.")
        sys.exit(1)
    
    # Generate report
    report = detector.generate_report(results, args.format)
    
    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()


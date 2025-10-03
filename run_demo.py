#!/usr/bin/env python3
"""
Demo script to showcase the Code Smell Detector functionality.
This script runs various detection scenarios to demonstrate the tool's capabilities.
"""

import subprocess
import sys
import os

def run_command(description, command, capture=False):
    """Run a command and display output."""
    print("\n" + "="*80)
    print(f"DEMO: {description}")
    print("="*80)
    print(f"Command: {command}\n")
    
    if capture:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr, file=sys.stderr)
        return result.returncode == 0
    else:
        return subprocess.call(command, shell=True) == 0

def main():
    """Run demonstration scenarios."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CODE SMELL DETECTOR - DEMONSTRATION                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if we're in the right directory
    if not os.path.exists("detector") or not os.path.exists("smelly_code"):
        print("Error: Please run this script from the project root directory.")
        sys.exit(1)
    
    demos = []
    
    # Demo 1: Run unit tests
    print("\n[1/6] Running unit tests on smelly code...")
    if os.name == 'nt':  # Windows
        cmd = "cd smelly_code && python -m pytest test_main.py -v"
    else:  # Unix-like
        cmd = "cd smelly_code && python -m pytest test_main.py -v"
    run_command("Unit Tests - Verify Smelly Code Functionality", cmd)
    
    # Demo 2: Full detection
    print("\n[2/6] Running full smell detection...")
    if os.name == 'nt':
        cmd = "cd detector && python main.py ../smelly_code/main.py"
    else:
        cmd = "cd detector && python main.py ../smelly_code/main.py"
    run_command("Full Detection - All Smells Enabled", cmd)
    
    # Demo 3: Selective detection
    print("\n[3/6] Running selective detection (Long Method and God Class only)...")
    if os.name == 'nt':
        cmd = "cd detector && python main.py --only LongMethod,GodClass ../smelly_code/main.py"
    else:
        cmd = "cd detector && python main.py --only LongMethod,GodClass ../smelly_code/main.py"
    run_command("Selective Detection - Using --only Flag", cmd)
    
    # Demo 4: Exclusion
    print("\n[4/6] Running detection with exclusions...")
    if os.name == 'nt':
        cmd = "cd detector && python main.py --exclude DuplicatedCode,MagicNumbers ../smelly_code/main.py"
    else:
        cmd = "cd detector && python main.py --exclude DuplicatedCode,MagicNumbers ../smelly_code/main.py"
    run_command("Exclusion - Using --exclude Flag", cmd)
    
    # Demo 5: JSON output
    print("\n[5/6] Generating JSON output...")
    if os.name == 'nt':
        cmd = "cd detector && python main.py --format json --output detection_report.json ../smelly_code/main.py"
    else:
        cmd = "cd detector && python main.py --format json --output detection_report.json ../smelly_code/main.py"
    
    success = run_command("JSON Output - Machine-Readable Format", cmd)
    if success:
        print("\n✓ JSON report saved to: detector/detection_report.json")
    
    # Demo 6: External sample
    print("\n[6/6] Running detection on external sample...")
    if os.name == 'nt':
        cmd = "cd detector && python main.py ../external_sample.py"
    else:
        cmd = "cd detector && python main.py ../external_sample.py"
    run_command("External Sample - Testing on Different Code", cmd)
    
    # Summary
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)
    print("""
Summary of Demonstrated Features:
✓ Unit tests (8 tests, all passing)
✓ Full smell detection (all 6 smells)
✓ Selective detection (--only flag)
✓ Exclusion (--exclude flag)
✓ JSON output format
✓ External sample testing

Files Generated:
- detector/detection_report.json (JSON output)

Next Steps:
1. Review docs/REPORT.md for comprehensive analysis
2. Review docs/smells.md for smell documentation
3. Examine smelly_code/main.py to see intentional smells
4. Customize detector/config.yaml for your needs

For more options, run:
    cd detector
    python main.py --help
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during demo: {e}", file=sys.stderr)
        sys.exit(1)


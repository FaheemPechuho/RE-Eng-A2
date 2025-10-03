# Code Smell Detector

A Python application that detects common code smells in Python source code. This project includes both a deliberately "smelly" program for testing and a comprehensive detection tool.

## Project Structure

```
code/
├── smelly_code/
│   ├── main.py              # Deliberately smelly program (Student Grade Management System)
│   └── test_main.py         # Unit tests for the smelly program
├── detector/
│   ├── main.py              # Main entry point for the detector
│   ├── config.yaml          # Configuration file for detectors
│   └── detectors/
│       ├── __init__.py
│       ├── base_detector.py       # Base class for all detectors
│       ├── long_method.py         # Long Method detector
│       ├── god_class.py           # God Class detector
│       ├── duplicated_code.py     # Duplicated Code detector
│       ├── large_parameter_list.py # Large Parameter List detector
│       ├── magic_numbers.py       # Magic Numbers detector
│       └── feature_envy.py        # Feature Envy detector
├── docs/
│   └── smells.md            # Documentation of intentional code smells
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Features

### Detected Code Smells

1. **Long Method**: Methods exceeding a configurable line threshold
2. **God Class (Blob)**: Classes with too many methods or lines
3. **Duplicated Code**: Similar or identical code blocks
4. **Large Parameter List**: Methods with too many parameters
5. **Magic Numbers**: Hard-coded numeric literals without context
6. **Feature Envy**: Methods accessing other classes' data excessively

### Detector Features

- **Configurable Thresholds**: Customize detection sensitivity via `config.yaml`
- **CLI Override Options**: 
  - `--only`: Run only specified detectors
  - `--exclude`: Exclude specific detectors
- **Multiple Output Formats**: Text and JSON output
- **File or Directory Analysis**: Analyze single files or entire directories
- **Detailed Reports**: Line numbers, descriptions, and severity levels

## Installation

1. Clone the repository or extract the project files
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Detector

**Basic usage:**
```bash
cd detector
python main.py ../smelly_code/main.py
```

**Analyze a directory:**
```bash
python main.py ../smelly_code/
```

**Run only specific detectors:**
```bash
python main.py --only LongMethod,MagicNumbers ../smelly_code/main.py
```

**Exclude specific detectors:**
```bash
python main.py --exclude DuplicatedCode ../smelly_code/main.py
```

**Custom configuration file:**
```bash
python main.py --config custom_config.yaml ../smelly_code/main.py
```

**JSON output:**
```bash
python main.py --format json ../smelly_code/main.py
```

**Save report to file:**
```bash
python main.py --output report.txt ../smelly_code/main.py
```

### Configuration

Edit `detector/config.yaml` to customize detector behavior:

```yaml
detectors:
  LongMethod:
    enabled: true
    threshold: 30  # Lines
  
  GodClass:
    enabled: true
    method_threshold: 10
    line_threshold: 150
  
  DuplicatedCode:
    enabled: true
    min_lines: 5
    similarity_threshold: 0.85
  
  LargeParameterList:
    enabled: true
    threshold: 5
  
  MagicNumbers:
    enabled: true
    allowed_numbers: [0, 1, -1, 2]
  
  FeatureEnvy:
    enabled: true
    external_call_ratio: 0.6
    min_external_calls: 3
```

### CLI Priority

Command-line arguments override configuration file settings:
1. `--only` flag: Runs ONLY specified detectors (highest priority)
2. `--exclude` flag: Runs all enabled detectors EXCEPT specified ones
3. Config file: Default behavior when no CLI flags provided

## Running Tests

Test the smelly code functionality:

```bash
cd smelly_code
python -m pytest test_main.py -v
```

Or run the smelly program directly:

```bash
python main.py
```

## Deliberately Smelly Code

The `smelly_code/main.py` file contains a Student Grade Management System with intentionally introduced code smells:

- **Lines 37-72**: Long Method (add_student_with_validation_and_logging)
- **Lines 29-193**: God Class (GradeManagementSystem)
- **Multiple locations**: Duplicated validation and logging code
- **Lines 74-88**: Large Parameter List (calculate_weighted_grade with 6 parameters)
- **Various lines**: Magic Numbers (15, 18, 90, 80, 70, 60, etc.)
- **Lines 128-160**: Feature Envy (calculate_student_statistics)

See `docs/smells.md` for detailed documentation of each smell.

## Detection Logic & Thresholds

### Long Method
- **Threshold**: 30 lines (configurable)
- **Logic**: Counts lines between method definition and end
- **Rationale**: Methods over 30 lines typically do too much and should be refactored

### God Class
- **Method Threshold**: 10 methods (configurable)
- **Line Threshold**: 150 lines (configurable)
- **Logic**: Counts methods and total lines in class definition
- **Rationale**: Classes exceeding either threshold likely violate Single Responsibility Principle

### Duplicated Code
- **Minimum Lines**: 5 (configurable)
- **Similarity Threshold**: 85% (configurable)
- **Logic**: Uses SequenceMatcher to compare code blocks, normalized for whitespace
- **Rationale**: High similarity indicates copy-paste programming that increases maintenance burden

### Large Parameter List
- **Threshold**: 5 parameters (configurable)
- **Logic**: Counts method parameters (excluding self/cls)
- **Rationale**: Methods with many parameters are hard to understand and use; suggests need for parameter objects

### Magic Numbers
- **Allowed Numbers**: [0, 1, -1, 2] (configurable)
- **Logic**: Detects numeric literals in code, excluding allowed values
- **Rationale**: Hard-coded numbers lack context; should be named constants

### Feature Envy
- **External Call Ratio**: 60% (configurable)
- **Minimum External Calls**: 3 (configurable)
- **Logic**: Counts attribute/method accesses to external objects vs. self
- **Rationale**: Methods primarily using another class's data suggest misplaced responsibility

## Example Output

```
================================================================================
CODE SMELL DETECTION REPORT
================================================================================
Generated: 2025-10-03 14:30:00
Active Detectors: LongMethod, GodClass, DuplicatedCode, LargeParameterList, MagicNumbers, FeatureEnvy
================================================================================

File: ../smelly_code/main.py
  Total Smells: 12

  LongMethod (1 instance(s)):
    - lines 37-72 [high]
      Method 'add_student_with_validation_and_logging' has 36 lines, exceeding threshold of 30 lines

  GodClass (1 instance(s)):
    - lines 29-193 [high]
      Class 'GradeManagementSystem' is a God Class with 15 methods (threshold: 10), 165 lines (threshold: 150)

  LargeParameterList (1 instance(s)):
    - lines 74-88 [high]
      Method 'calculate_weighted_grade' has 6 parameters (threshold: 5). Parameters: self, student_id, homework_weight, midterm_weight, final_weight, participation_weight, project_weight

  MagicNumbers (6 instance(s)):
    - line 46 [low]
      Magic number(s) found: [15, 100]. Consider using named constants for better readability
    - line 49 [low]
      Magic number(s) found: [18]. Consider using named constants for better readability
    ...

  DuplicatedCode (2 instance(s)):
    - lines 37-126 [medium]
      Duplicated code between methods 'add_student_with_validation_and_logging' (lines 37-72) and 'update_student_email' (lines 90-109). Similarity: 68%
    ...

  FeatureEnvy (1 instance(s)):
    - lines 128-160 [medium]
      Method 'calculate_student_statistics' in class 'GradeManagementSystem' shows feature envy. 5/6 (83.3%) attribute accesses are to external objects. Most accessed: 'student' (5 times)

--------------------------------------------------------------------------------

================================================================================
SUMMARY: 12 total code smell(s) detected
================================================================================
```

## Technical Debt & Maintainability Impact

Code smells indicate areas of technical debt that impact:

1. **Maintainability**: Smelly code is harder to modify and extend
2. **Readability**: Code becomes difficult for new developers to understand
3. **Testing**: Complex methods and classes are harder to test thoroughly
4. **Bugs**: Duplicated code and magic numbers increase error probability
5. **Evolution**: God classes and feature envy resist architectural changes

Regular smell detection helps teams identify refactoring priorities and maintain code quality over time.



# Code Smells Documentation

This document lists all intentionally introduced code smells in the Student Grade Management System (`smelly_code/main.py`).

## 1. Long Method

**Location**: `smelly_code/main.py`, Lines 37-72

**Method**: `add_student_with_validation_and_logging()`

**Justification**: This method has 36 lines and performs multiple responsibilities including validation of student ID, name, age, and email, creating the student object, adding initial grades, storing the student, and logging the action. This violates the Single Responsibility Principle and makes the method hard to test and maintain.

---

## 2. God Class (Blob)

**Location**: `smelly_code/main.py`, Lines 29-193

**Class**: `GradeManagementSystem`

**Justification**: This class has 15 methods and over 160 lines, handling multiple unrelated responsibilities: student management, grade calculation, email updates, student removal, statistics calculation, course management, enrollment, file I/O, and history tracking. This violates the Single Responsibility Principle. The class should be split into separate classes like StudentRepository, GradeCalculator, CourseManager, and Logger.

---

## 3. Duplicated Code

**Location**: 
- `smelly_code/main.py`, Lines 37-72 (`add_student_with_validation_and_logging()`)
- `smelly_code/main.py`, Lines 90-109 (`update_student_email()`)
- `smelly_code/main.py`, Lines 111-126 (`remove_student()`)

**Justification**: The validation logic for student ID (lines 38-41, 91-94, 113-116) and email validation (lines 49-51, 96-98) are duplicated across multiple methods. Additionally, the logging pattern (creating a log_entry dictionary and appending to grade_history) appears in lines 63-70, 103-108, and 120-125. This code duplication makes maintenance difficult as changes need to be replicated across multiple locations.

---

## 4. Large Parameter List

**Location**: `smelly_code/main.py`, Lines 74-88

**Method**: `calculate_weighted_grade()`

**Justification**: This method takes 6 parameters (student_id, homework_weight, midterm_weight, final_weight, participation_weight, project_weight). Having this many parameters makes the method difficult to call, understand, and maintain. It would be better to use a parameter object or configuration dictionary.

---

## 5. Magic Numbers

**Locations**:
- Line 46: Age validation uses hard-coded values 15 and 100
- Line 49: Age check uses hard-coded value 18
- Line 55: Grade validation uses hard-coded values 0 and 100
- Line 79: Checks if grades list has at least 5 elements
- Lines 81-85: Uses hard-coded indices 0, 1, 2, 3, 4 for grades array access
- Lines 143-152: Grade letter calculation uses hard-coded thresholds 90, 80, 70, 60

**Justification**: These hard-coded numeric literals lack context and make the code harder to understand and maintain. Values like 15, 18, 100 for age ranges, 90, 80, 70, 60 for grade thresholds should be defined as named constants (e.g., MIN_AGE, MAX_AGE, ADULT_AGE, GRADE_A_THRESHOLD) to improve readability and maintainability.

---

## 6. Feature Envy

**Location**: `smelly_code/main.py`, Lines 128-160

**Method**: `calculate_student_statistics()`

**Justification**: This method in the GradeManagementSystem class extensively accesses the Student object's data through getter methods (get_grades() on line 136, get_name() on line 158). The method performs 5 operations on student data (getting grades, calculating average, max, min, and accessing name) but only 1 operation on its own class data (checking if student_id exists). The ratio of external calls to internal operations indicates that this functionality would be better placed in the Student class itself, as it primarily manipulates Student data.

---

## Summary

All six code smells have been deliberately introduced to demonstrate common anti-patterns in software development. Despite these smells, the program runs correctly and all unit tests pass, illustrating how code can be functionally correct yet structurally problematic from a maintainability perspective.


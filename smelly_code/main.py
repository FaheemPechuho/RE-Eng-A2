"""
Student Grade Management System
A deliberately smelly program for code smell detection testing.
"""

import json
from datetime import datetime


class Student:
    """Simple student data class."""
    def __init__(self, student_id, name, age, email):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.email = email
        self.grades = []
    
    def get_id(self):
        return self.student_id
    
    def get_name(self):
        return self.name
    
    def get_grades(self):
        return self.grades
    
    def add_grade(self, grade):
        self.grades.append(grade)


# God Class (Blob) - does everything: manages students, grades, reports, persistence, validation
class GradeManagementSystem:
    """Main system class that handles all operations."""
    
    def __init__(self):
        self.students = {}
        self.courses = {}
        self.grade_history = []
    
    # Long Method - intentionally long method with many responsibilities
    def add_student_with_validation_and_logging(self, student_id, name, age, email, initial_grades=None):
        """Add a student with comprehensive validation and logging."""
        # Validate student ID
        if not student_id or not isinstance(student_id, str):
            return False
        if student_id in self.students:
            return False
        
        # Validate name
        if not name or len(name) < 2 or len(name) > 50:
            return False
        
        # Validate age (Magic Numbers - 15, 100, 18)
        if not age or age < 15 or age > 100:
            return False
        
        # Check if adult
        is_adult = age >= 18
        
        # Validate email
        if not email or '@' not in email or '.' not in email:
            return False
        
        # Create student object
        student = Student(student_id, name, age, email)
        
        # Add initial grades if provided
        if initial_grades:
            for grade in initial_grades:
                if 0 <= grade <= 100:  # Magic Numbers
                    student.add_grade(grade)
        
        # Add to system
        self.students[student_id] = student
        
        # Log the action
        log_entry = {
            'action': 'add_student',
            'student_id': student_id,
            'timestamp': str(datetime.now()),
            'is_adult': is_adult
        }
        self.grade_history.append(log_entry)
        
        return True
    
    # Large Parameter List - method with 6 parameters
    def calculate_weighted_grade(self, student_id, homework_weight, midterm_weight, final_weight, participation_weight, project_weight):
        """Calculate weighted grade with multiple components."""
        if student_id not in self.students:
            return None
        
        student = self.students[student_id]
        grades = student.get_grades()
        
        if len(grades) < 5:  # Magic Number
            return None
        
        weighted = (grades[0] * homework_weight + 
                   grades[1] * midterm_weight + 
                   grades[2] * final_weight + 
                   grades[3] * participation_weight + 
                   grades[4] * project_weight)
        
        return weighted
    
    # Duplicated Code - similar validation logic repeated
    def update_student_email(self, student_id, new_email):
        """Update student email with validation."""
        if not student_id or not isinstance(student_id, str):
            return False
        if student_id not in self.students:
            return False
        
        # Validate email (duplicated from add_student)
        if not new_email or '@' not in new_email or '.' not in new_email:
            return False
        
        student = self.students[student_id]
        student.email = new_email
        
        # Log the action (duplicated logging pattern)
        log_entry = {
            'action': 'update_email',
            'student_id': student_id,
            'timestamp': str(datetime.now())
        }
        self.grade_history.append(log_entry)
        
        return True
    
    # Duplicated Code - more similar validation
    def remove_student(self, student_id):
        """Remove a student from the system."""
        if not student_id or not isinstance(student_id, str):
            return False
        if student_id not in self.students:
            return False
        
        del self.students[student_id]
        
        # Log the action (duplicated logging pattern)
        log_entry = {
            'action': 'remove_student',
            'student_id': student_id,
            'timestamp': str(datetime.now())
        }
        self.grade_history.append(log_entry)
        
        return True
    
    # Feature Envy - this method uses Student's data extensively
    def calculate_student_statistics(self, student_id):
        """Calculate statistics for a student."""
        if student_id not in self.students:
            return None
        
        student = self.students[student_id]
        
        # Heavy use of student's internal data (Feature Envy)
        grades = student.get_grades()
        if not grades:
            return None
        
        avg = sum(grades) / len(grades)
        max_grade = max(grades)
        min_grade = min(grades)
        
        # Magic Numbers - 90, 80, 70, 60
        if avg >= 90:
            letter_grade = 'A'
        elif avg >= 80:
            letter_grade = 'B'
        elif avg >= 70:
            letter_grade = 'C'
        elif avg >= 60:
            letter_grade = 'D'
        else:
            letter_grade = 'F'
        
        return {
            'average': avg,
            'max': max_grade,
            'min': min_grade,
            'letter_grade': letter_grade,
            'student_name': student.get_name()
        }
    
    def get_student(self, student_id):
        """Get a student by ID."""
        return self.students.get(student_id)
    
    def get_all_students(self):
        """Get all students."""
        return list(self.students.values())
    
    def add_course(self, course_id, course_name, credits):
        """Add a course to the system."""
        self.courses[course_id] = {
            'name': course_name,
            'credits': credits,
            'enrolled_students': []
        }
    
    def enroll_student(self, student_id, course_id):
        """Enroll a student in a course."""
        if student_id in self.students and course_id in self.courses:
            self.courses[course_id]['enrolled_students'].append(student_id)
            return True
        return False
    
    def save_to_file(self, filename):
        """Save system data to file."""
        data = {
            'students': {sid: {
                'id': s.student_id,
                'name': s.name,
                'age': s.age,
                'email': s.email,
                'grades': s.grades
            } for sid, s in self.students.items()},
            'courses': self.courses
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_history_count(self):
        """Get count of history entries."""
        return len(self.grade_history)


def main():
    """Main entry point."""
    system = GradeManagementSystem()
    
    # Add some test students
    system.add_student_with_validation_and_logging('S001', 'Alice Johnson', 20, 'alice@example.com', [85, 90, 88, 92, 87])
    system.add_student_with_validation_and_logging('S002', 'Bob Smith', 19, 'bob@example.com', [78, 82, 80, 75, 79])
    system.add_student_with_validation_and_logging('S003', 'Charlie Brown', 21, 'charlie@example.com', [95, 93, 96, 94, 95])
    
    # Calculate statistics
    stats = system.calculate_student_statistics('S001')
    if stats:
        print(f"Student: {stats['student_name']}")
        print(f"Average: {stats['average']:.2f}")
        print(f"Letter Grade: {stats['letter_grade']}")
    
    # Calculate weighted grade (0.2, 0.25, 0.35, 0.1, 0.1)
    weighted = system.calculate_weighted_grade('S002', 0.2, 0.25, 0.35, 0.1, 0.1)
    if weighted:
        print(f"\nWeighted grade for Bob: {weighted:.2f}")
    
    print(f"\nTotal students: {len(system.get_all_students())}")
    print(f"History entries: {system.get_history_count()}")


if __name__ == '__main__':
    main()


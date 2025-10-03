"""
Unit tests for the Student Grade Management System.
These tests validate the functionality despite code smells.
"""

import unittest
import os
from main import GradeManagementSystem, Student


class TestStudentGradeManagementSystem(unittest.TestCase):
    """Test cases for the grade management system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.system = GradeManagementSystem()
    
    def test_add_student_success(self):
        """Test successfully adding a valid student."""
        result = self.system.add_student_with_validation_and_logging(
            'S001', 'John Doe', 20, 'john@example.com', [85, 90, 88]
        )
        self.assertTrue(result)
        student = self.system.get_student('S001')
        self.assertIsNotNone(student)
        self.assertEqual(student.get_name(), 'John Doe')
        self.assertEqual(len(student.get_grades()), 3)
    
    def test_add_student_invalid_age(self):
        """Test adding student with invalid age."""
        result = self.system.add_student_with_validation_and_logging(
            'S002', 'Jane Doe', 12, 'jane@example.com'
        )
        self.assertFalse(result)
        self.assertIsNone(self.system.get_student('S002'))
    
    def test_add_student_invalid_email(self):
        """Test adding student with invalid email."""
        result = self.system.add_student_with_validation_and_logging(
            'S003', 'Bob Smith', 19, 'invalidemail'
        )
        self.assertFalse(result)
    
    def test_calculate_weighted_grade(self):
        """Test weighted grade calculation."""
        self.system.add_student_with_validation_and_logging(
            'S004', 'Alice Brown', 21, 'alice@example.com', [80, 85, 90, 75, 88]
        )
        weighted = self.system.calculate_weighted_grade('S004', 0.2, 0.25, 0.35, 0.1, 0.1)
        self.assertIsNotNone(weighted)
        expected = 80 * 0.2 + 85 * 0.25 + 90 * 0.35 + 75 * 0.1 + 88 * 0.1
        self.assertAlmostEqual(weighted, expected, places=2)
    
    def test_update_student_email(self):
        """Test updating student email."""
        self.system.add_student_with_validation_and_logging(
            'S005', 'Charlie Davis', 22, 'charlie@example.com'
        )
        result = self.system.update_student_email('S005', 'new.charlie@example.com')
        self.assertTrue(result)
        student = self.system.get_student('S005')
        self.assertEqual(student.email, 'new.charlie@example.com')
    
    def test_calculate_student_statistics(self):
        """Test student statistics calculation."""
        self.system.add_student_with_validation_and_logging(
            'S006', 'Diana Evans', 20, 'diana@example.com', [92, 95, 93, 90, 94]
        )
        stats = self.system.calculate_student_statistics('S006')
        self.assertIsNotNone(stats)
        self.assertEqual(stats['letter_grade'], 'A')
        self.assertGreater(stats['average'], 90)
        self.assertEqual(stats['max'], 95)
        self.assertEqual(stats['min'], 90)
    
    def test_remove_student(self):
        """Test removing a student."""
        self.system.add_student_with_validation_and_logging(
            'S007', 'Eve Foster', 19, 'eve@example.com'
        )
        self.assertIsNotNone(self.system.get_student('S007'))
        result = self.system.remove_student('S007')
        self.assertTrue(result)
        self.assertIsNone(self.system.get_student('S007'))
    
    def test_course_enrollment(self):
        """Test course creation and student enrollment."""
        self.system.add_student_with_validation_and_logging(
            'S008', 'Frank Green', 21, 'frank@example.com'
        )
        self.system.add_course('CS101', 'Introduction to Programming', 3)
        result = self.system.enroll_student('S008', 'CS101')
        self.assertTrue(result)
        self.assertIn('S008', self.system.courses['CS101']['enrolled_students'])


if __name__ == '__main__':
    unittest.main()


#!/usr/bin/env python3
"""
Test runner script for the Mathtermind project.
Run this script to execute all tests.
"""

import unittest
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import test modules
from tests.ui.services.test_course_service import TestCourseService
from tests.ui.widgets.test_search_bar import TestSearchBar
from tests.ui.widgets.test_courses_grid import TestCoursesGrid
from tests.ui.pages.test_courses_page import TestCoursePage


def create_test_suite():
    """Create a test suite containing all tests"""
    test_suite = unittest.TestSuite()
    
    # Add test cases for services
    test_suite.addTest(unittest.makeSuite(TestCourseService))
    
    # Add test cases for widgets
    test_suite.addTest(unittest.makeSuite(TestSearchBar))
    test_suite.addTest(unittest.makeSuite(TestCoursesGrid))
    
    # Add test cases for pages
    test_suite.addTest(unittest.makeSuite(TestCoursePage))
    
    return test_suite


if __name__ == '__main__':
    # Create the test suite
    suite = create_test_suite()
    
    # Create a test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the tests
    result = runner.run(suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful()) 
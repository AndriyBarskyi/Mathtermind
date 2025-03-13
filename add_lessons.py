"""
Script to add new lessons to existing courses.
"""

from src.db.seed_courses import seed_courses

if __name__ == "__main__":
    # Force add new lessons to existing courses
    seed_courses(force_add_lessons=True) 
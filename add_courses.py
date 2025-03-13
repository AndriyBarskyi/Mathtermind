#!/usr/bin/env python3
"""
Script to add courses and lessons to the database.
Run this script to populate the database with sample courses and lessons.
"""

from src.db.seed_courses import seed_courses

if __name__ == "__main__":
    print("Adding courses and lessons to the database...")
    seed_courses(force_add_lessons=True)
    print("Done!") 
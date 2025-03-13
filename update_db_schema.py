#!/usr/bin/env python3
"""
Script to update the database schema to match the models.
This script will drop and recreate the lessons table.
"""

import sqlite3
from src.db import get_db, init_db
from src.db.models import Base, Lesson
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def update_lessons_table():
    """Update the lessons table schema to match the model."""
    print("Updating lessons table schema...")
    
    # Connect to the database
    conn = sqlite3.connect('mathtermind.db')
    cursor = conn.cursor()
    
    # Backup existing lessons data
    print("Backing up existing lessons data...")
    cursor.execute("SELECT * FROM lessons")
    existing_lessons = cursor.fetchall()
    
    # Drop the existing lessons table
    print("Dropping existing lessons table...")
    cursor.execute("DROP TABLE IF EXISTS lessons")
    conn.commit()
    
    # Recreate the lessons table with the correct schema
    print("Recreating lessons table with correct schema...")
    engine = create_engine('sqlite:///mathtermind.db')
    Base.metadata.create_all(engine, tables=[Lesson.__table__])
    
    # Restore lessons data if possible
    if existing_lessons:
        print(f"Found {len(existing_lessons)} existing lessons to restore.")
        # We need to adapt the data to the new schema
        # This is a simplified example - you may need to adjust based on your actual data
        for lesson in existing_lessons:
            try:
                # Map old columns to new columns
                # Assuming the order: id, course_id, title, content, lesson_type, lesson_order, created_at
                cursor.execute("""
                    INSERT INTO lessons (id, course_id, title, content, lesson_type, lesson_order, created_at, 
                                        difficulty_level, estimated_time, points_reward, prerequisites, 
                                        adaptive_rules, learning_objectives)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    lesson[0],  # id
                    lesson[1],  # course_id
                    lesson[2],  # title
                    lesson[3],  # content
                    lesson[4],  # lesson_type
                    lesson[5],  # lesson_order
                    lesson[6],  # created_at
                    'Beginner',  # default difficulty_level
                    30,  # default estimated_time (30 minutes)
                    10,  # default points_reward
                    '{"required_lessons": [], "required_concepts": []}',  # default prerequisites
                    '{"difficulty_adjustment": {"increase_if": {"consecutive_correct": 3, "time_under": 15}, "decrease_if": {"consecutive_wrong": 2, "time_over": 45}}, "reinforcement_triggers": {"wrong_attempts": 2, "time_threshold": 30}}',  # default adaptive_rules
                    '[]'  # default learning_objectives
                ))
                print(f"Restored lesson: {lesson[2]}")
            except Exception as e:
                print(f"Error restoring lesson {lesson[2]}: {str(e)}")
    
    conn.commit()
    conn.close()
    print("Lessons table schema updated successfully!")

if __name__ == "__main__":
    update_lessons_table() 
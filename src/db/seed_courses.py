"""
Seed script for populating the database with sample course data.

This script creates sample courses and lessons in the database for development
and testing purposes.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any

from sqlalchemy.orm import Session

from src.db import get_db
from src.db.models import Course, Lesson
from src.db.models.enums import Topic
from src.core import get_logger
from src.core.error_handling import handle_db_errors

logger = get_logger(__name__)

@handle_db_errors(operation="seed_courses")
def seed_courses():
    """
    Seed the database with sample course data.
    """
    logger.info("Seeding courses...")
    
    # Get database session
    db = next(get_db())
    
    # Check if courses already exist
    existing_courses = db.query(Course).count()
    if existing_courses > 0:
        logger.info(f"Found {existing_courses} existing courses. Skipping seeding.")
        return
    
    # Create sample courses
    courses = [
        {
            "id": uuid.uuid4(),
            "topic": Topic.MATHEMATICS,
            "name": "Базова математика",
            "description": "Курс з основ математики для початківців",
            "duration": 120,  # in minutes
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.MATHEMATICS,
            "name": "Алгебра і функції",
            "description": "Вивчення алгебраїчних функцій, графіків та рівнянь",
            "duration": 180,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.MATHEMATICS,
            "name": "Вища математика",
            "description": "Поглиблене вивчення математичних концепцій",
            "duration": 240,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.INFORMATICS,
            "name": "Основи програмування",
            "description": "Вступ до програмування та алгоритмів",
            "duration": 150,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.INFORMATICS,
            "name": "Структури даних",
            "description": "Вивчення основних структур даних та їх застосування",
            "duration": 200,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.INFORMATICS,
            "name": "Розробка веб-додатків",
            "description": "Створення веб-додатків з використанням сучасних технологій",
            "duration": 300,
            "created_at": datetime.now(timezone.utc),
        },
    ]
    
    # Create and save course objects
    course_objects = []
    for course_data in courses:
        course = Course(**course_data)
        db.add(course)
        course_objects.append(course)
    
    # Commit to database
    db.commit()
    logger.info(f"Created {len(courses)} sample courses")
    
    # Create sample lessons for each course
    _seed_lessons(db, course_objects)
    
    logger.info("Course and lesson seeding completed successfully")


def _seed_lessons(db: Session, courses: List[Course]):
    """
    Seed the database with sample lessons for each course.
    
    Args:
        db: The database session
        courses: List of course objects to create lessons for
    """
    logger.info("Seeding lessons for courses...")
    
    # Create 3-5 lessons for each course
    lessons_count = 0
    
    for i, course in enumerate(courses):
        # Number of lessons varies by course
        num_lessons = 3 if i % 3 == 0 else 4 if i % 3 == 1 else 5
        
        for j in range(1, num_lessons + 1):
            lesson = Lesson(
                id=uuid.uuid4(),
                course_id=course.id,
                title=f"Урок {j}: {_get_lesson_title(course.topic, j, i % 3)}",
                lesson_order=j,
                estimated_time=30,  # in minutes
                points_reward=100,
                created_at=datetime.now(timezone.utc)
            )
            db.add(lesson)
            lessons_count += 1
    
    db.commit()
    logger.info(f"Created {lessons_count} sample lessons")


def _get_lesson_title(topic: Topic, lesson_number: int, level: int) -> str:
    """
    Generate a relevant lesson title based on the course topic and lesson number.
    
    Args:
        topic: The course topic
        lesson_number: The lesson number
        level: Difficulty level (0: beginner, 1: intermediate, 2: advanced)
        
    Returns:
        A lesson title
    """
    math_lessons = {
        0: [  # Beginner
            "Числа та арифметичні операції",
            "Дроби та відсотки",
            "Геометричні фігури"
        ],
        1: [  # Intermediate
            "Лінійні рівняння",
            "Функції та графіки",
            "Квадратні рівняння",
            "Системи рівнянь"
        ],
        2: [  # Advanced
            "Тригонометрія",
            "Похідні функцій",
            "Інтеграли",
            "Диференціальні рівняння",
            "Комплексні числа"
        ]
    }
    
    info_lessons = {
        0: [  # Beginner
            "Алгоритми та блок-схеми",
            "Змінні та типи даних",
            "Умови та цикли"
        ],
        1: [  # Intermediate
            "Масиви та списки",
            "Функції та методи",
            "Хеш-таблиці",
            "Графи та дерева"
        ],
        2: [  # Advanced
            "HTML, CSS, JavaScript",
            "Фреймворки та бібліотеки",
            "Бази даних",
            "Серверна частина",
            "Розгортання додатків"
        ]
    }
    
    if lesson_number <= 0:
        return "Вступ до курсу"
    
    if topic == Topic.MATHEMATICS:
        lessons = math_lessons.get(level, [])
    else:
        lessons = info_lessons.get(level, [])
    
    if lesson_number <= len(lessons):
        return lessons[lesson_number - 1]
    else:
        return f"Додатковий матеріал {lesson_number - len(lessons)}" 
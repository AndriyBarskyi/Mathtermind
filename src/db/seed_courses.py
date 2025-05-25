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
        # Math courses
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
            "topic": Topic.MATHEMATICS,
            "name": "Статистика та аналіз даних",
            "description": "Вивчення статистичних методів та аналізу даних",
            "duration": 200,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.MATHEMATICS,
            "name": "Геометрія та топологія",
            "description": "Курс з геометрії у просторі та основ топології",
            "duration": 190,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.MATHEMATICS,
            "name": "Теорія ймовірностей",
            "description": "Основи теорії ймовірностей та стохастичні процеси",
            "duration": 160,
            "created_at": datetime.now(timezone.utc),
        },
        # Informatics courses
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
        {
            "id": uuid.uuid4(),
            "topic": Topic.INFORMATICS,
            "name": "Бази даних та SQL",
            "description": "Проєктування та робота з базами даних",
            "duration": 180,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.INFORMATICS,
            "name": "Машинне навчання",
            "description": "Основи машинного навчання та штучного інтелекту",
            "duration": 250,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.INFORMATICS,
            "name": "Мобільна розробка",
            "description": "Створення додатків для мобільних платформ",
            "duration": 220,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.INFORMATICS,
            "name": "Кібербезпека для початківців",
            "description": "Основи кібербезпеки, захист даних та приватність в Інтернеті.",
            "duration": 120,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.MATHEMATICS,
            "name": "Теорія графів та її застосування",
            "description": "Вступ до теорії графів, алгоритми на графах та їх практичне використання.",
            "duration": 180,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.INFORMATICS,
            "name": "Python для аналізу даних",
            "description": "Використання Python та бібліотек Pandas, NumPy, Matplotlib для аналізу та візуалізації даних.",
            "duration": 240,
            "created_at": datetime.now(timezone.utc),
        },
        {
            "id": uuid.uuid4(),
            "topic": Topic.MATHEMATICS,
            "name": "Вступ до математичного моделювання",
            "description": "Побудова математичних моделей для розв'язання реальних задач.",
            "duration": 150,
            "created_at": datetime.now(timezone.utc),
        }
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
    
    # Create lessons for each course - vary the number of lessons by course
    lessons_count = 0
    
    for i, course in enumerate(courses):
        # Number of lessons varies by course (4-8 lessons per course)
        num_lessons = 4 + (i % 5)  # This will create courses with 4, 5, 6, 7, or 8 lessons
        
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
            "Геометричні фігури",
            "Основи алгебри",
            "Розв'язування простих рівнянь",
            "Пропорції та відношення",
            "Вимірювання та одиниці виміру",
            "Основи теорії множин",
        ],
        1: [  # Intermediate
            "Лінійні рівняння",
            "Функції та графіки",
            "Квадратні рівняння",
            "Системи рівнянь",
            "Тригонометричні функції",
            "Вектори та матриці",
            "Логарифми та експоненти",
            "Статистичні методи",
        ],
        2: [  # Advanced
            "Тригонометрія",
            "Похідні функцій",
            "Інтеграли",
            "Диференціальні рівняння",
            "Комплексні числа",
            "Аналітична геометрія",
            "Теорія груп",
            "Числові ряди",
        ]
    }
    
    info_lessons = {
        0: [  # Beginner
            "Алгоритми та блок-схеми",
            "Змінні та типи даних",
            "Умови та цикли",
            "Основи функцій",
            "Робота з файлами",
            "Масиви та списки",
            "Основи об'єктно-орієнтованого програмування",
            "Введення та виведення даних",
        ],
        1: [  # Intermediate
            "Масиви та списки",
            "Функції та методи",
            "Хеш-таблиці",
            "Графи та дерева",
            "Рекурсивні алгоритми",
            "Обробка винятків",
            "Основи мережевого програмування",
            "Робота з базами даних",
        ],
        2: [  # Advanced
            "HTML, CSS, JavaScript",
            "Фреймворки та бібліотеки",
            "Бази даних",
            "Серверна частина",
            "Розгортання додатків",
            "Безпека веб-додатків",
            "RESTful API",
            "Мікросервісна архітектура",
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
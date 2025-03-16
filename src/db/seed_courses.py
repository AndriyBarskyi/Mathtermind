"""
Script to seed the database with sample courses and lessons.
Run this script to populate the database with sample data for testing.
"""

from src.db import get_db
from src.db.repositories import course_repo
from src.db.models import Lesson
import uuid
from datetime import datetime, timezone
import json


def seed_courses(force_add_lessons=False):
    """
    Seed the database with sample courses and lessons.
    
    Args:
        force_add_lessons: If True, add new lessons to courses even if they already have lessons
    """
    db = next(get_db())
    
    # Check if courses already exist
    existing_courses = course_repo.get_all_courses(db)
    if existing_courses:
        print(f"Database already contains {len(existing_courses)} courses. Skipping course seeding.")
        
        # Check if lessons exist
        try:
            has_lessons = False
            for course in existing_courses:
                course_lessons = db.query(Lesson).filter(Lesson.course_id == course.id).all()
                if course_lessons:
                    has_lessons = True
                    break
        except Exception as e:
            print(f"Error checking for lessons: {str(e)}")
            has_lessons = False
        
        if not has_lessons or force_add_lessons:
            if not has_lessons:
                print("No lessons found. Adding lessons to existing courses.")
            else:
                print("Force adding new lessons to existing courses.")
            
            add_lessons_to_courses(db, existing_courses)
        else:
            print(f"Lessons already exist. Skipping lesson seeding.")
        
        return
    
    # Sample course data
    course_templates = [
        {
            "topic": "INFORMATICS",
            "name": "Вступ до машинного навчання",
            "description": "Цей курс надає базові знання з машинного навчання, включаючи класифікацію, регресію та кластеризацію. Ви навчитеся застосовувати алгоритми машинного навчання для вирішення реальних задач.",
            "difficulty_level": "Beginner",
            "target_age_group": "15-17",
            "estimated_time": 300,  # 5 hours in minutes
            "points_reward": 100,
            "prerequisites": {
                "required_courses": [],
                "required_skills": ["Базові знання з програмування", "Основи математики"],
                "minimum_level": 1
            },
            "tags": ["Машинне навчання", "Базовий", "Інтерактивний", "Новий"]
        },
        {
            "topic": "INFORMATICS",
            "name": "Алгоритми та структури даних",
            "description": "Вивчення основних алгоритмів та структур даних, їх аналіз та застосування в програмуванні. Курс охоплює сортування, пошук, графи, дерева та інші важливі концепції.",
            "difficulty_level": "Intermediate",
            "target_age_group": "15-17",
            "estimated_time": 480,  # 8 hours in minutes
            "points_reward": 150,
            "prerequisites": {
                "required_courses": [],
                "required_skills": ["Програмування на Python або C++", "Основи математики"],
                "minimum_level": 2
            },
            "tags": ["Алгоритми", "Структури даних", "Середній", "Інтерактивний"]
        },
        {
            "topic": "MATHEMATICS",
            "name": "Лінійна алгебра",
            "description": "Основи лінійної алгебри, включаючи вектори, матриці, лінійні перетворення та їх застосування. Курс надає теоретичні знання та практичні навички для розв'язання задач.",
            "difficulty_level": "Beginner",
            "target_age_group": "15-17",
            "estimated_time": 360,  # 6 hours in minutes
            "points_reward": 120,
            "prerequisites": {
                "required_courses": [],
                "required_skills": ["Базові знання з математики"],
                "minimum_level": 1
            },
            "tags": ["Лінійна алгебра", "Матриці", "Вектори", "Базовий", "Теоретичний"]
        },
        {
            "topic": "INFORMATICS",
            "name": "Глибоке навчання",
            "description": "Поглиблене вивчення нейронних мереж, включаючи CNN, RNN, трансформери та їх застосування. Курс охоплює теоретичні основи та практичні аспекти глибокого навчання.",
            "difficulty_level": "Advanced",
            "target_age_group": "15-17",
            "estimated_time": 720,  # 12 hours in minutes
            "points_reward": 200,
            "prerequisites": {
                "required_courses": [],
                "required_skills": ["Машинне навчання", "Python", "Лінійна алгебра"],
                "minimum_level": 3
            },
            "tags": ["Глибоке навчання", "Нейронні мережі", "Просунутий", "Практичний"]
        },
        {
            "topic": "MATHEMATICS",
            "name": "Математичний аналіз",
            "description": "Вивчення диференціального та інтегрального числення, границь, рядів та їх застосування. Курс надає фундаментальні знання з математичного аналізу.",
            "difficulty_level": "Intermediate",
            "target_age_group": "15-17",
            "estimated_time": 600,  # 10 hours in minutes
            "points_reward": 180,
            "prerequisites": {
                "required_courses": [],
                "required_skills": ["Алгебра", "Геометрія"],
                "minimum_level": 2
            },
            "tags": ["Математичний аналіз", "Диференціальне числення", "Інтегральне числення", "Середній", "Теоретичний"]
        },
        {
            "topic": "INFORMATICS",
            "name": "Веб-розробка",
            "description": "Вивчення основ веб-розробки, включаючи HTML, CSS, JavaScript та сучасні фреймворки. Курс надає практичні навички для створення веб-сайтів та веб-додатків.",
            "difficulty_level": "Beginner",
            "target_age_group": "13-14",
            "estimated_time": 420,  # 7 hours in minutes
            "points_reward": 130,
            "prerequisites": {
                "required_courses": [],
                "required_skills": ["Базові знання з програмування"],
                "minimum_level": 1
            },
            "tags": ["Веб-розробка", "HTML", "CSS", "JavaScript", "Базовий", "Практичний", "Новий"]
        }
    ]
    
    # Create courses
    created_courses = []
    for course_template in course_templates:
        course = course_repo.create_course(
            db,
            topic=course_template["topic"],
            name=course_template["name"],
            description=course_template["description"],
            difficulty_level=course_template["difficulty_level"],
            target_age_group=course_template["target_age_group"],
            estimated_time=course_template["estimated_time"],
            points_reward=course_template["points_reward"],
            prerequisites=course_template["prerequisites"],
            tags=course_template["tags"]
        )
        created_courses.append(course)
    
    print(f"Created {len(created_courses)} courses.")
    
    # Add lessons to courses
    add_lessons_to_courses(db, created_courses)


def add_lessons_to_courses(db, courses):
    """
    Add sample lessons to courses.
    
    Args:
        db: Database session
        courses: List of course objects to add lessons to
    """
    total_lessons_added = 0
    
    for course in courses:
        # Define lessons for each course
        lesson_templates = generate_lesson_templates_for_course(course)
        
        # Check if this course already has lessons
        try:
            existing_lessons = db.query(Lesson).filter(Lesson.course_id == course.id).all()
            existing_lesson_orders = [lesson.lesson_order for lesson in existing_lessons]
        except Exception as e:
            print(f"Error checking for existing lessons: {str(e)}")
            existing_lesson_orders = []
        
        # Add lessons to database
        for lesson_template in lesson_templates:
            # Skip if a lesson with this order already exists
            if lesson_template["lesson_order"] in existing_lesson_orders:
                continue
                
            try:
                # Use default difficulty level
                course_difficulty = "Beginner"
                
                # Create lesson with only the columns that exist in the schema
                new_lesson = Lesson(
                    id=uuid.uuid4(),
                    course_id=course.id,
                    title=lesson_template["title"],
                    lesson_type=lesson_template["lesson_type"],
                    difficulty_level=course_difficulty,
                    lesson_order=lesson_template["lesson_order"],
                    estimated_time=30,  # Default 30 minutes
                    points_reward=10,  # Default 10 points
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
                db.add(new_lesson)
                db.commit()  # Commit each lesson individually to avoid rollback issues
                
                # Now create content for the lesson if needed
                if "content" in lesson_template:
                    # Here you would add code to create content objects
                    # This would depend on your Content model structure
                    pass
                
                total_lessons_added += 1
                print(f"Added lesson: {lesson_template['title']}")
            except Exception as e:
                print(f"Error adding lesson: {str(e)}")
                db.rollback()  # Rollback on error
    
    print(f"Added {total_lessons_added} new lessons to {len(courses)} courses.")


def generate_lesson_templates_for_course(course):
    """
    Generate sample lesson templates for a specific course.
    
    Args:
        course: Course object to generate lessons for
        
    Returns:
        List of lesson template dictionaries
    """
    # Default difficulty level
    course_difficulty = "Beginner"
    
    if course.topic == "INFORMATICS" and "машинного навчання" in course.name:
        return [
            {
                "title": "Вступ до нейронних мереж",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Що таке нейронні мережі",
                                "content": "Нейронні мережі - це обчислювальні системи, натхненні біологічними нейронними мережами мозку тварин. У цьому уроці ви дізнаєтесь про основні принципи роботи нейронних мереж та їх застосування."
                            }
                        ]
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": course_difficulty,
                "lesson_order": 1
            },
            {
                "title": "Огляд генеративних змагальних мереж",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Що таке GAN",
                                "content": "Генеративні змагальні мережі (GAN) - це клас алгоритмів машинного навчання, які використовуються для генерації нових даних, схожих на навчальні. У цьому уроці ви дізнаєтесь про принципи роботи GAN та їх застосування."
                            }
                        ]
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": course_difficulty,
                "lesson_order": 2
            },
            {
                "title": "Інструменти та програмне забезпечення для ШІ",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Огляд інструментів",
                                "content": "У цьому уроці ми розглянемо популярні інструменти для роботи з ШІ, такі як TensorFlow, PyTorch, Keras та інші. Ви дізнаєтесь про їх особливості та сфери застосування."
                            }
                        ]
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": course_difficulty,
                "lesson_order": 3
            }
        ]
    elif course.topic == "INFORMATICS" and "Алгоритми" in course.name:
        return [
            {
                "title": "Основи алгоритмів",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Що таке алгоритм",
                                "content": "Алгоритм - це послідовність чітко визначених інструкцій для вирішення певної задачі. У цьому уроці ви дізнаєтесь про основні властивості алгоритмів та їх класифікацію."
                            }
                        ]
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": course_difficulty,
                "lesson_order": 1
            },
            {
                "title": "Структури даних: масиви та списки",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Масиви та списки",
                                "content": "Масиви та списки - це базові структури даних, які використовуються для зберігання та організації даних. У цьому уроці ви дізнаєтесь про їх особливості та операції над ними."
                            }
                        ]
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": course_difficulty,
                "lesson_order": 2
            },
            {
                "title": "Алгоритми сортування",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Основні алгоритми сортування",
                                "content": "У цьому уроці ми розглянемо основні алгоритми сортування, такі як бульбашкове сортування, сортування вставками, швидке сортування та інші. Ви дізнаєтесь про їх принципи роботи та ефективність."
                            }
                        ]
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": course_difficulty,
                "lesson_order": 3
            }
        ]
    else:
        # Default lessons for other courses
        return [
            {
                "title": f"Урок 1: Вступ до {course.name}",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Вступ",
                                "content": f"Це вступний урок до курсу {course.name}. У цьому уроці ви дізнаєтесь про основні поняття та принципи, які будуть розглянуті в курсі."
                            }
                        ]
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": course_difficulty,
                "lesson_order": 1
            },
            {
                "title": f"Урок 2: Основні концепції {course.name}",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Основні концепції",
                                "content": f"У цьому уроці ми розглянемо основні концепції {course.name}, які є фундаментальними для розуміння подальшого матеріалу."
                            }
                        ]
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": course_difficulty,
                "lesson_order": 2
            },
            {
                "title": f"Урок 3: Практичне застосування {course.name}",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Практичне застосування",
                                "content": f"У цьому уроці ми розглянемо практичне застосування {course.name} на реальних прикладах. Ви зможете застосувати отримані знання для вирішення практичних задач."
                            }
                        ]
                    },
                    "practice": {
                        "exercises": [
                            {
                                "question": "Виконайте практичне завдання",
                                "type": "open_ended",
                                "options": [],
                                "solution": "",
                                "hints": ["Використовуйте знання з попередніх уроків"]
                            }
                        ]
                    }
                },
                "lesson_type": "EXERCISE",
                "difficulty_level": course_difficulty,
                "lesson_order": 3
            }
        ]


if __name__ == "__main__":
    seed_courses() 
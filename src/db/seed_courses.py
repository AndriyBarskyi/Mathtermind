"""
Script to seed the database with sample courses.
Run this script to populate the database with sample courses for testing.
"""

from src.db import get_db
from src.db.repositories import course_repo


def seed_courses():
    """Seed the database with sample courses."""
    db = next(get_db())
    
    # Check if courses already exist
    existing_courses = course_repo.get_all_courses(db)
    if existing_courses:
        print(f"Database already contains {len(existing_courses)} courses. Skipping seeding.")
        return
    
    # Sample courses
    courses = [
        {
            "topic": "Informatics",
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
            "topic": "Informatics",
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
            "topic": "Math",
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
            "topic": "Informatics",
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
            "topic": "Math",
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
            "topic": "Informatics",
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
    
    # Add courses to the database
    for course_data in courses:
        try:
            course_repo.create_course(db, **course_data)
            print(f"Added course: {course_data['name']}")
        except Exception as e:
            print(f"Error adding course {course_data['name']}: {str(e)}")
    
    print(f"Successfully added courses to the database.")


if __name__ == "__main__":
    seed_courses() 
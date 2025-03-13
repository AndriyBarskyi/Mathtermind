"""
Script to seed the database with sample courses.
Run this script to populate the database with sample courses for testing.
"""

from src.db import get_db
from src.db.repositories import course_repo
from src.db.models import Lesson
import uuid
from datetime import datetime, timezone
import json


def seed_courses(force_add_lessons=False):
    """
    Seed the database with sample courses.
    
    Args:
        force_add_lessons: If True, add new lessons to courses even if they already have lessons
    """
    db = next(get_db())
    
    # Check if courses already exist
    existing_courses = course_repo.get_all_courses(db)
    if existing_courses:
        print(f"Database already contains {len(existing_courses)} courses. Skipping seeding.")
        
        # Check if lessons exist
        has_lessons = any(course.lessons for course in existing_courses)
        
        if not has_lessons or force_add_lessons:
            if not has_lessons:
                print("No lessons found. Adding lessons to existing courses.")
            else:
                print("Force adding new lessons to existing courses.")
            
            add_lessons_to_courses(db, existing_courses)
        else:
            print(f"Lessons already exist. Skipping lesson seeding.")
        
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
    
    # Create courses
    created_courses = []
    for course_data in courses:
        course = course_repo.create_course(
            db,
            topic=course_data["topic"],
            name=course_data["name"],
            description=course_data["description"],
            difficulty_level=course_data["difficulty_level"],
            target_age_group=course_data["target_age_group"],
            estimated_time=course_data["estimated_time"],
            points_reward=course_data["points_reward"],
            prerequisites=course_data["prerequisites"],
            tags=course_data["tags"]
        )
        created_courses.append(course)
    
    print(f"Created {len(created_courses)} courses.")
    
    # Add lessons to courses
    add_lessons_to_courses(db, created_courses)


def add_lessons_to_courses(db, courses):
    """Add sample lessons to courses."""
    total_lessons = 0
    
    for course in courses:
        # Define lessons for each course
        lessons = create_lessons_for_course(course)
        
        # Check if this course already has lessons
        existing_lessons = db.query(Lesson).filter(Lesson.course_id == course.id).all()
        existing_lesson_orders = [lesson.lesson_order for lesson in existing_lessons]
        
        # Add lessons to database
        for lesson_data in lessons:
            # Skip if a lesson with this order already exists
            if lesson_data["lesson_order"] in existing_lesson_orders:
                continue
                
            lesson = Lesson(
                id=uuid.uuid4(),
                course_id=course.id,
                title=lesson_data["title"],
                content=lesson_data["content"],
                lesson_type=lesson_data["lesson_type"],
                difficulty_level=lesson_data["difficulty_level"],
                lesson_order=lesson_data["lesson_order"],
                estimated_time=lesson_data["estimated_time"],
                points_reward=lesson_data["points_reward"],
                prerequisites=lesson_data["prerequisites"],
                learning_objectives=lesson_data["learning_objectives"]
            )
            db.add(lesson)
            total_lessons += 1
    
    db.commit()
    print(f"Added {total_lessons} new lessons to {len(courses)} courses.")


def create_lessons_for_course(course):
    """Create sample lessons for a specific course."""
    if course.topic == "Informatics" and "машинного навчання" in course.name:
        return [
            {
                "title": "Вступ до нейронних мереж",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Що таке нейронні мережі",
                                "content": "Нейронні мережі - це обчислювальні системи, натхненні біологічними нейронними мережами мозку тварин...",
                                "examples": []
                            }
                        ],
                        "resources": [
                            {
                                "type": "video",
                                "url": "https://example.com/video1",
                                "description": "Вступ до нейронних мереж"
                            }
                        ]
                    },
                    "practice": {
                        "exercises": []
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": "Beginner",
                "lesson_order": 1,
                "estimated_time": 45,
                "points_reward": 10,
                "prerequisites": {},
                "learning_objectives": ["Розуміння основ нейронних мереж"]
            },
            {
                "title": "Огляд генеративних змагальних мереж",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Що таке GAN",
                                "content": "Генеративні змагальні мережі (GAN) - це клас алгоритмів машинного навчання...",
                                "examples": []
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": []
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": "Intermediate",
                "lesson_order": 2,
                "estimated_time": 45,
                "points_reward": 15,
                "prerequisites": {},
                "learning_objectives": ["Розуміння принципів роботи GAN"]
            },
            {
                "title": "Інструменти та програмне забезпечення для ШІ",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Огляд інструментів",
                                "content": "У цьому уроці ми розглянемо популярні інструменти для роботи з ШІ...",
                                "examples": []
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": []
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": "Beginner",
                "lesson_order": 3,
                "estimated_time": 45,
                "points_reward": 10,
                "prerequisites": {},
                "learning_objectives": ["Знайомство з інструментами для ШІ"]
            },
            {
                "title": "Генерація зображень за допомогою ШІ",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Методи генерації зображень",
                                "content": "У цьому уроці ми розглянемо методи генерації зображень за допомогою ШІ...",
                                "examples": []
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": [
                            {
                                "question": "Створіть просте зображення за допомогою ШІ",
                                "type": "open_ended",
                                "options": [],
                                "solution": "",
                                "hints": ["Використовуйте інструменти, які ми розглянули в уроці"]
                            }
                        ]
                    }
                },
                "lesson_type": "Practice",
                "difficulty_level": "Intermediate",
                "lesson_order": 4,
                "estimated_time": 60,
                "points_reward": 20,
                "prerequisites": {},
                "learning_objectives": ["Практичні навички генерації зображень"]
            },
            {
                "title": "Основи класифікації в машинному навчанні",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Що таке класифікація",
                                "content": "Класифікація - це задача машинного навчання, яка полягає у віднесенні об'єкта до однієї з категорій на основі його характеристик...",
                                "examples": [
                                    {
                                        "description": "Приклад класифікації електронних листів",
                                        "code": "from sklearn.naive_bayes import MultinomialNB\nclf = MultinomialNB()\nclf.fit(X_train, y_train)\npredictions = clf.predict(X_test)",
                                        "output": "Accuracy: 0.92"
                                    }
                                ]
                            }
                        ],
                        "resources": [
                            {
                                "type": "video",
                                "url": "https://example.com/classification_intro",
                                "description": "Вступ до класифікації"
                            }
                        ]
                    },
                    "practice": {
                        "exercises": [
                            {
                                "question": "Реалізуйте простий класифікатор для розпізнавання рукописних цифр",
                                "type": "code",
                                "options": [],
                                "solution": "from sklearn.neighbors import KNeighborsClassifier\nclf = KNeighborsClassifier()\nclf.fit(X_train, y_train)",
                                "hints": ["Використовуйте KNN або SVM класифікатор"]
                            }
                        ]
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": "Beginner",
                "lesson_order": 5,
                "estimated_time": 50,
                "points_reward": 15,
                "prerequisites": {},
                "learning_objectives": ["Розуміння основ класифікації", "Вміння використовувати базові класифікатори"]
            },
            {
                "title": "Регресійний аналіз",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Лінійна регресія",
                                "content": "Лінійна регресія - це метод моделювання залежності між скалярною величиною y та одним або декількома незалежними змінними X...",
                                "examples": [
                                    {
                                        "description": "Приклад лінійної регресії",
                                        "code": "from sklearn.linear_model import LinearRegression\nmodel = LinearRegression()\nmodel.fit(X_train, y_train)\npredictions = model.predict(X_test)",
                                        "output": "R²: 0.85"
                                    }
                                ]
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": [
                            {
                                "question": "Реалізуйте модель лінійної регресії для прогнозування цін на нерухомість",
                                "type": "code",
                                "options": [],
                                "solution": "",
                                "hints": ["Використовуйте sklearn.linear_model.LinearRegression"]
                            }
                        ]
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": "Intermediate",
                "lesson_order": 6,
                "estimated_time": 55,
                "points_reward": 20,
                "prerequisites": {},
                "learning_objectives": ["Розуміння регресійного аналізу", "Вміння будувати регресійні моделі"]
            },
            {
                "title": "Кластеризація даних",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Методи кластеризації",
                                "content": "Кластеризація - це задача розбиття множини об'єктів на групи (кластери) таким чином, щоб об'єкти в одному кластері були більш схожі між собою, ніж з об'єктами з інших кластерів...",
                                "examples": []
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": []
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": "Intermediate",
                "lesson_order": 7,
                "estimated_time": 50,
                "points_reward": 15,
                "prerequisites": {},
                "learning_objectives": ["Розуміння методів кластеризації"]
            },
            {
                "title": "Оцінка моделей машинного навчання",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Метрики оцінки",
                                "content": "Для оцінки якості моделей машинного навчання використовуються різні метрики, такі як точність, повнота, F1-міра, ROC-крива та інші...",
                                "examples": []
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": [
                            {
                                "question": "Обчисліть точність, повноту та F1-міру для моделі класифікації",
                                "type": "code",
                                "options": [],
                                "solution": "from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score\naccuracy = accuracy_score(y_true, y_pred)\nprecision = precision_score(y_true, y_pred)\nrecall = recall_score(y_true, y_pred)\nf1 = f1_score(y_true, y_pred)",
                                "hints": ["Використовуйте функції з модуля sklearn.metrics"]
                            }
                        ]
                    }
                },
                "lesson_type": "Practice",
                "difficulty_level": "Intermediate",
                "lesson_order": 8,
                "estimated_time": 60,
                "points_reward": 25,
                "prerequisites": {},
                "learning_objectives": ["Розуміння метрик оцінки моделей", "Вміння оцінювати якість моделей"]
            },
            {
                "title": "Фінальний проект: Створення моделі машинного навчання",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Вимоги до проекту",
                                "content": "У цьому фінальному проекті ви створите повноцінну модель машинного навчання для вирішення реальної задачі...",
                                "examples": []
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": [
                            {
                                "question": "Створіть модель машинного навчання для вирішення обраної вами задачі",
                                "type": "open_ended",
                                "options": [],
                                "solution": "",
                                "hints": ["Використовуйте знання, отримані протягом курсу"]
                            }
                        ]
                    }
                },
                "lesson_type": "Challenge",
                "difficulty_level": "Advanced",
                "lesson_order": 9,
                "estimated_time": 120,
                "points_reward": 50,
                "prerequisites": {},
                "learning_objectives": ["Застосування знань з машинного навчання на практиці", "Створення повноцінної моделі машинного навчання"]
            }
        ]
    elif course.topic == "Informatics" and "Алгоритми" in course.name:
        return [
            {
                "title": "Основи алгоритмів",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Що таке алгоритм",
                                "content": "Алгоритм - це послідовність чітко визначених інструкцій...",
                                "examples": []
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": []
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": "Beginner",
                "lesson_order": 1,
                "estimated_time": 45,
                "points_reward": 10,
                "prerequisites": {},
                "learning_objectives": ["Розуміння основ алгоритмів"]
            },
            {
                "title": "Структури даних: масиви та списки",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Масиви та списки",
                                "content": "Масиви та списки - це базові структури даних...",
                                "examples": []
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": []
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": "Beginner",
                "lesson_order": 2,
                "estimated_time": 45,
                "points_reward": 10,
                "prerequisites": {},
                "learning_objectives": ["Розуміння масивів та списків"]
            },
            {
                "title": "Алгоритми сортування",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Основні алгоритми сортування",
                                "content": "У цьому уроці ми розглянемо основні алгоритми сортування...",
                                "examples": []
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": []
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": "Intermediate",
                "lesson_order": 3,
                "estimated_time": 60,
                "points_reward": 15,
                "prerequisites": {},
                "learning_objectives": ["Розуміння алгоритмів сортування"]
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
                                "content": f"Це вступний урок до курсу {course.name}...",
                                "examples": []
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": []
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": "Beginner",
                "lesson_order": 1,
                "estimated_time": 45,
                "points_reward": 10,
                "prerequisites": {},
                "learning_objectives": [f"Розуміння основ {course.name}"]
            },
            {
                "title": f"Урок 2: Основні концепції {course.name}",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Основні концепції",
                                "content": f"У цьому уроці ми розглянемо основні концепції {course.name}...",
                                "examples": []
                            }
                        ],
                        "resources": []
                    },
                    "practice": {
                        "exercises": []
                    }
                },
                "lesson_type": "Theory",
                "difficulty_level": "Beginner",
                "lesson_order": 2,
                "estimated_time": 45,
                "points_reward": 10,
                "prerequisites": {},
                "learning_objectives": [f"Розуміння основних концепцій {course.name}"]
            },
            {
                "title": f"Урок 3: Практичне застосування {course.name}",
                "content": {
                    "theory": {
                        "sections": [
                            {
                                "title": "Практичне застосування",
                                "content": f"У цьому уроці ми розглянемо практичне застосування {course.name}...",
                                "examples": []
                            }
                        ],
                        "resources": []
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
                "lesson_type": "Practice",
                "difficulty_level": "Intermediate",
                "lesson_order": 3,
                "estimated_time": 60,
                "points_reward": 15,
                "prerequisites": {},
                "learning_objectives": [f"Практичні навички застосування {course.name}"]
            }
        ]


if __name__ == "__main__":
    seed_courses() 
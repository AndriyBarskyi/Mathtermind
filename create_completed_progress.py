from src.db import get_db
from src.db.repositories import progress_repo
import uuid
from datetime import datetime, timezone
from src.db.models import User, Course, Lesson, Progress

# Create a completed progress record for a user
db = next(get_db())

# Get the first user
user = db.query(User).first()
if not user:
    print('No users found')
    exit()

# Get the second course (to have a different one from the first script)
courses = db.query(Course).all()
if len(courses) < 2:
    print('Not enough courses found')
    exit()

course = courses[1]  # Get the second course

# Get the first lesson of the course
lesson = db.query(Lesson).filter(Lesson.course_id == course.id).first()
if not lesson:
    print('No lessons found for course')
    exit()

# Check if progress record already exists
existing_progress = db.query(Progress).filter(
    Progress.user_id == user.id,
    Progress.course_id == course.id
).first()

if existing_progress:
    print(f'Progress record already exists for user {user.id} and course {course.id}')
    print(f'Current progress: {existing_progress.progress_percentage}%')
    
    # Update to completed
    existing_progress.progress_percentage = 100.0
    existing_progress.last_accessed = datetime.now(timezone.utc)
    db.commit()
    print(f'Updated progress to 100%')
    exit()

# Create a completed progress record
progress = Progress(
    id=uuid.uuid4(),
    user_id=user.id,
    course_id=course.id,
    current_lesson_id=lesson.id,
    completed_lessons=[],
    current_difficulty="Beginner",
    progress_percentage=100.0,  # 100% complete
    total_points_earned=150,
    time_spent=180,  # 180 minutes
    strengths=[],
    weaknesses=[],
    learning_path={
        "current_path": [str(lesson.id)],
        "recommended_next": [],
        "mastery_goals": {}
    },
    progress_data={
        "quiz_attempts": [],
        "practice_sessions": []
    },
    last_accessed=datetime.now(timezone.utc)
)

# Save the progress record
db.add(progress)
db.commit()
print(f'Created completed progress record for user {user.id} and course {course.id}')
print(f'User: {user.username} ({user.email})')
print(f'Course: {course.name}')
print(f'Progress: 100%') 
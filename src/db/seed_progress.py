"""
Seed script for populating the database with sample progress data.

This script creates sample progress records, completed lessons, and completed courses
for development and testing purposes.
"""

import uuid
from datetime import datetime, timezone, timedelta
import random
from typing import List, Dict, Any

from sqlalchemy.orm import Session

from src.db import get_db
from src.db.models import (
    User, Course, Lesson, Progress, CompletedLesson, 
    CompletedCourse, UserContentProgress, ContentState, Content
)
from src.core import get_logger
from src.core.error_handling import handle_db_errors

logger = get_logger(__name__)

@handle_db_errors(operation="seed_progress")
def seed_progress():
    """
    Seed the database with sample progress data for the admin user.
    """
    logger.info("Seeding progress data...")
    
    # Get database session
    db = next(get_db())
    
    # Check if progress data already exists
    existing_progress = db.query(Progress).count()
    if existing_progress > 0:
        logger.info(f"Found {existing_progress} existing progress records. Skipping seeding.")
        return
    
    # Get admin user
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        logger.warning("Admin user not found. Skipping progress seeding.")
        return
    
    # Get all courses
    courses = db.query(Course).all()
    if not courses:
        logger.warning("No courses found. Skipping progress seeding.")
        return
    
    # Create progress for each course for admin user
    _seed_course_progress(db, admin_user, courses)
    
    logger.info("Progress data seeding completed successfully")


def _seed_course_progress(db: Session, user: User, courses: List[Course]):
    """
    Seed progress data for each course for the given user.
    
    Args:
        db: Database session
        user: User to create progress for
        courses: List of courses
    """
    logger.info(f"Creating progress data for user {user.username}...")
    
    # Randomize which courses are completed, in progress, or just started
    random.shuffle(courses)
    
    num_courses = len(courses)
    num_to_leave_unstarted = min(3, num_courses) # Leave up to 3 courses unstarted, or fewer if not enough courses
    
    # Define slices ensuring they don't overlap and handle small numbers of courses
    idx_completed_end = min(2, num_courses - num_to_leave_unstarted) # Max 2 completed, but leave space for unstarted
    idx_in_progress_end = min(idx_completed_end + 3, num_courses - num_to_leave_unstarted) # Max 3 in-progress
    idx_started_end = num_courses - num_to_leave_unstarted # All remaining that are not unstarted

    completed_courses = courses[:idx_completed_end]
    in_progress_courses = courses[idx_completed_end:idx_in_progress_end]
    # Only assign to started_courses if there's a valid range
    started_courses = []
    if idx_in_progress_end < idx_started_end:
        started_courses = courses[idx_in_progress_end:idx_started_end]
    
    unstarted_course_names = [c.name for c in courses[idx_started_end:]]
    if unstarted_course_names:
        logger.info(f"The following courses will be intentionally left unstarted: {', '.join(unstarted_course_names)}")
    else:
        logger.info("No courses will be left unstarted (either too few courses or all assigned progress).")

    # Create completed course progress
    for course in completed_courses:
        _create_completed_course_progress(db, user, course)
    
    # Create in-progress course progress
    for course in in_progress_courses:
        _create_in_progress_course_progress(db, user, course)
    
    # Create just started course progress
    for course in started_courses:
        _create_started_course_progress(db, user, course)
    
    db.commit()
    logger.info(f"Created progress data for {len(courses)} courses")


def _seed_user_content_activity(db: Session, user: User, course: Course, days_ago_max: int, items_to_complete: int):
    logger.info(f"Seeding content activity for user {user.username}, course {course.name}...")
    lessons = db.query(Lesson).filter(Lesson.course_id == course.id).all()
    if not lessons:
        logger.warning(f"No lessons found for course {course.name} to seed content activity.")
        return

    all_content_items = []
    for lesson in lessons:
        content_items = db.query(Content).filter(Content.lesson_id == lesson.id).all()
        all_content_items.extend(content_items)

    if not all_content_items:
        logger.warning(f"No content items found in course {course.name} to seed activity.")
        return

    # Ensure we don't try to complete more items than available
    items_to_complete = min(items_to_complete, len(all_content_items))
    
    # Get the main progress record for this course and user to link UserContentProgress
    course_progress_record = db.query(Progress).filter(
        Progress.user_id == user.id,
        Progress.course_id == course.id
    ).first()

    if not course_progress_record:
        logger.warning(f"No main progress record found for user {user.id} and course {course.id}. Skipping content activity seeding.")
        return


    completed_count = 0
    for _ in range(items_to_complete):
        content_item = random.choice(all_content_items)
        
        # Check if progress for this content item already exists
        existing_ucp = db.query(UserContentProgress).filter(
            UserContentProgress.user_id == user.id,
            UserContentProgress.content_id == content_item.id
        ).first()

        if existing_ucp:
            # Optionally update it if needed, or just skip
            # For simplicity, we'll skip if it already exists to avoid complex update logic here
            # logger.info(f"Content item {content_item.id} already has progress for user {user.id}. Skipping.")
            continue

        days_offset = random.randint(0, days_ago_max -1) # 0 for today, up to days_ago_max-1 for oldest
        # Ensure completion_time is aware, as UserContentProgress.updated_at expects
        completion_time = datetime.now(timezone.utc) - timedelta(days=days_offset, hours=random.randint(0,23), minutes=random.randint(0,59))

        ucp = UserContentProgress(
            id=uuid.uuid4(),
            user_id=user.id,
            content_id=content_item.id,
            is_completed=True,
            score=random.uniform(70, 100) if content_item.content_type in ["assessment", "quiz", "exercise"] else None,
            time_spent=random.randint(5, 30) * 60,  # 5-30 minutes in seconds
            last_interaction=completion_time,
            # 'updated_at' and 'created_at' will be set by the model/Base if not provided or use default
            # Explicitly setting updated_at to ensure it matches our desired completion time for the graph
            # However, UserContentProgress model might not have updated_at as a direct field in constructor
            # Base model has it. Let's rely on last_interaction primarily for the "completion event time"
            # and ensure the DB model handles created_at/updated_at appropriately.
            # The get_all_completed_by_user in repo sorts by UserContentProgress.updated_at.
            # So, we need to make sure this field is effectively our completion_time.
            # If UserContentProgress inherits from a base model that auto-sets updated_at on creation/commit,
            # then we should use that. For now, we set last_interaction.
            # Let's check UserContentProgress model definition again later if needed.
            # For now, assume last_interaction is a good proxy if updated_at isn't directly settable here or works automatically.
            # Re-checking the repo: it orders by `UserContentProgress.updated_at`.
            # `UserContentProgress` model directly has `updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))`
            # So `updated_at` will be set on creation/update. To control it for seeding, we might need to pass it, or it will be "now".
            # Let's try setting it explicitly to completion_time if the model allows.
            # The UserContentProgress constructor in user_content_progress_repo.py does not take updated_at or created_at.
            # This means it relies on the DB model defaults.
            # We'll use last_interaction for our logic and hope updated_at is close enough or sort by last_interaction later.
            # The UI graph currently uses 'updated_at' from the UserContentProgress model.
            # Let's try to directly set updated_at after creation for seeding.
            # No, that's bad practice. The UserContentProgress model should handle it.
            # The repository query sorts by `updated_at`. We need to make sure `updated_at` reflects the historical completion.
            # The `Base` model has `created_at` and `updated_at` with defaults.
            # When a record is created, both are set. When updated, `updated_at` changes.
            # For seeding "historical" completions, this is tricky if `updated_at` auto-updates.
            # The easiest is to use `last_interaction` as the source of truth for activity time
            # and modify the UI to use that field.
            # OR, for seeding, we can create and then immediately update the record with a fake change to force updated_at. (hacky)
            # OR, the model should allow setting created_at/updated_at on creation for seeding.
            # Let's assume for now the `last_interaction` is the "completion time" we control.
            # We will change the UI to sort by `last_interaction` later if `updated_at` is problematic.
            # For now, will proceed with `last_interaction` as the controlled seed time.

            # The repo query `get_all_completed_by_user` sorts by `updated_at`.
            # This will make all seeded items appear as "today" if not careful.
            # Let's try to set `created_at` and `updated_at` in the constructor if the model allows it,
            # otherwise, this seeding strategy for past dates on `updated_at` won't work with current repo query.
            # The Pydantic model for UI might have `updated_at`. The DB model `UserContentProgress` has defaults.
            # The constructor in the REPO for `UserContentProgress` does NOT take created_at/updated_at.
            # So `updated_at` will be `datetime.now(timezone.utc)` when the seed runs.
            #
            # CONCLUSION for now: The activity graph sorting by `item.updated_at` in `main_win.py` will NOT work correctly with this seeding
            # unless we change how `updated_at` is set or change the sort field.
            # I will change `main_win.py` to use `item.last_interaction` for the date.

        )
        # Directly setting created_at and updated_at for seeding if the model columns are exposed
        # This is often done by passing them to the constructor if the SQLAlchemy model allows it
        # If not, this specific seeding for historical `updated_at` is hard.
        # Let's assume the model is like: `updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)`
        # We cannot easily override default on creation via the repo's create_progress.
        #
        # For now, I'll proceed with the structure, and we will fix the date field in main_win.py next.
        db.add(ucp)
        completed_count += 1
    
    if completed_count > 0:
        logger.info(f"Seeded {completed_count} content activity items for user {user.username}, course {course.name}.")


def _create_completed_course_progress(db: Session, user: User, course: Course):
    """Create progress data for a completed course."""
    # Get all lessons for the course
    lessons = db.query(Lesson).filter(Lesson.course_id == course.id).order_by(Lesson.lesson_order).all()
    if not lessons:
        return
    
    # Create progress record
    progress = Progress(
        id=uuid.uuid4(),
        user_id=user.id,
        course_id=course.id,
        current_lesson_id=None,  # No current lesson since course is completed
        total_points_earned=len(lessons) * 100,  # 100 points per lesson
        time_spent=len(lessons) * 30,  # 30 min per lesson
        progress_percentage=100.0,
        progress_data={
            "completed_lessons": len(lessons),
            "total_lessons": len(lessons),
            "average_score": random.randint(85, 100)
        },
        last_accessed=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 7)),
        is_completed=True
    )
    db.add(progress)
    
    # Mark all lessons as completed
    for i, lesson in enumerate(lessons):
        completed_date = datetime.now(timezone.utc) - timedelta(days=random.randint(10, 20) + (len(lessons) - i))
        score = random.randint(80, 100)
        time_spent = random.randint(25, 40)  # Minutes
        
        completed_lesson = CompletedLesson(
            id=uuid.uuid4(),
            user_id=user.id,
            lesson_id=lesson.id,
            course_id=course.id,
            completed_at=completed_date,
            score=score,
            time_spent=time_spent
        )
        db.add(completed_lesson)
    
    # Create completed course record
    completed_course = CompletedCourse(
        id=uuid.uuid4(),
        user_id=user.id,
        course_id=course.id,
        completed_at=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 5)),
        final_score=float(random.randint(85, 98)),
        total_time_spent=progress.time_spent,
        completed_lessons_count=len(lessons),
        achievements_earned=[str(uuid.uuid4()) for _ in range(random.randint(1, 3))],
        certificate_id=uuid.uuid4()
    )
    db.add(completed_course)

    # Seed content activity for this completed course
    _seed_user_content_activity(db, user, course, days_ago_max=7, items_to_complete=random.randint(5, 15))


def _create_in_progress_course_progress(db: Session, user: User, course: Course):
    """Create progress data for a course that is in progress (partially completed)."""
    # Get all lessons for the course
    lessons = db.query(Lesson).filter(Lesson.course_id == course.id).order_by(Lesson.lesson_order).all()
    if not lessons:
        return
    
    # Complete a random number of lessons (between 1 and total lessons - 1)
    if len(lessons) <= 1:
        num_lessons_to_complete = 0 # Cannot complete if only 1 or 0 lessons
    else:
        num_lessons_to_complete = random.randint(1, len(lessons) -1) if len(lessons) > 1 else 0

    # Create progress record
    progress = Progress(
        id=uuid.uuid4(),
        user_id=user.id,
        course_id=course.id,
        current_lesson_id=lessons[num_lessons_to_complete].id if num_lessons_to_complete < len(lessons) else lessons[-1].id,
        total_points_earned=num_lessons_to_complete * 100,  # 100 points per lesson
        time_spent=num_lessons_to_complete * 30,  # 30 min per lesson
        progress_percentage=round((num_lessons_to_complete / len(lessons)) * 100, 1),
        progress_data={
            "completed_lessons": num_lessons_to_complete,
            "total_lessons": len(lessons),
            "average_score": random.randint(75, 95)
        },
        last_accessed=datetime.now(timezone.utc) - timedelta(days=random.randint(0, 3)),
        is_completed=False
    )
    db.add(progress)
    
    # Mark some lessons as completed
    for i, lesson in enumerate(lessons):
        if i < num_lessons_to_complete:
            # For lessons considered "completed" within this in-progress course

            # Adjust completion dates:
            # Make roughly half of these recent (for activity graph), and others a bit older.
            if i < num_lessons_to_complete // 2: 
                 # These will be more recent for the activity graph
                 completed_at_offset = random.randint(0, 6) # 0-6 days ago
            else:
                 # These can be a bit older but still relatively recent for an "in-progress" course
                 completed_at_offset = random.randint(7, 20) # 7-20 days ago
            
            completed_at = datetime.now(timezone.utc) - timedelta(days=completed_at_offset, hours=random.randint(0,23))
            
            completed_lesson = CompletedLesson(
                id=uuid.uuid4(),
                user_id=user.id,
                lesson_id=lesson.id,
                course_id=course.id,
                completed_at=completed_at,
                score=random.randint(70, 100),
                time_spent=random.randint(20, 40)  # Minutes
            )
            db.add(completed_lesson)
    
    # Seed content activity for this in-progress course
    _seed_user_content_activity(db, user, course, days_ago_max=7, items_to_complete=random.randint(3, 10))


def _create_started_course_progress(db: Session, user: User, course: Course):
    """Create progress data for a course that has just been started."""
    # Get all lessons for the course
    lessons = db.query(Lesson).filter(Lesson.course_id == course.id).order_by(Lesson.lesson_order).all()
    if not lessons:
        return
    
    # Course just started, so only first lesson may be partially completed
    first_lesson = lessons[0]
    
    # Create progress record
    progress = Progress(
        id=uuid.uuid4(),
        user_id=user.id,
        course_id=course.id,
        current_lesson_id=first_lesson.id,
        total_points_earned=0,  # No points yet
        time_spent=random.randint(5, 15),  # Just started, minimal time spent
        progress_percentage=round((1 / len(lessons)) * random.uniform(0.1, 0.4) * 100, 1),  # Small percentage
        progress_data={
            "completed_lessons": 0,
            "total_lessons": len(lessons),
            "average_score": None
        },
        last_accessed=datetime.now(timezone.utc) - timedelta(days=random.randint(0, 2)),
        is_completed=False
    )
    db.add(progress)
    
    # Maybe add a content state for the first lesson
    if random.random() > 0.5:
        # Add a content state record to show partial progress
        content_state = ContentState(
            id=uuid.uuid4(),
            user_id=user.id,
            progress_id=progress.id,
            content_id=uuid.uuid4(),  # Placeholder - would need real content IDs
            state_type="scroll_position",
            numeric_value=random.uniform(0.1, 0.5),  # Percentage through content
            json_value=None,
            text_value=None,
            updated_at=datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48))
        )
        db.add(content_state) 
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

    # Ensure we have activity for each of the last 7 days
    # Distribute activities more evenly across days
    days = list(range(days_ago_max))
    
    # Make sure we have at least 1 activity for each day if there are enough items
    min_per_day = 1
    if items_to_complete >= days_ago_max * min_per_day:
        # Reserve some items to ensure each day has at least min_per_day activities
        reserved_items = days_ago_max * min_per_day
        remaining_items = items_to_complete - reserved_items
        
        # Assign the reserved items - one for each day
        day_assignments = {day: min_per_day for day in days}
        
        # Distribute remaining items randomly but with a bias toward more recent days
        # This creates a more realistic pattern with more activity in recent days
        weights = [1.5**((days_ago_max-day)/2) for day in days]  # Exponential weights - recent days get higher weight
        
        if remaining_items > 0:
            # Distribute remaining items based on weighted probability
            additional_assignments = random.choices(days, weights=weights, k=remaining_items)
            for day in additional_assignments:
                day_assignments[day] = day_assignments.get(day, 0) + 1
    else:
        # Not enough items for all days, distribute what we have
        # Bias toward recent days
        day_assignments = {day: 0 for day in days}
        assigned_days = random.choices(days, k=items_to_complete, 
                                      weights=[1.5**((days_ago_max-day)/2) for day in days])
        for day in assigned_days:
            day_assignments[day] = day_assignments.get(day, 0) + 1
    
    logger.info(f"Activity distribution plan for {course.name}: {day_assignments}")
    
    completed_count = 0
    
    # Process each day according to our plan
    for day, count in day_assignments.items():
        for _ in range(count):
            # Choose a random content item that doesn't already have progress
            available_items = []
            for content_item in all_content_items:
                existing_ucp = db.query(UserContentProgress).filter(
                    UserContentProgress.user_id == user.id,
                    UserContentProgress.content_id == content_item.id
                ).first()
                
                if not existing_ucp:
                    available_items.append(content_item)
            
            if not available_items:
                logger.warning(f"No more available content items for user {user.id} in course {course.id}.")
                break
                
            content_item = random.choice(available_items)
            
            # Calculate the completion time for this day
            completion_time = datetime.now(timezone.utc) - timedelta(
                days=day,
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            ucp = UserContentProgress(
                id=uuid.uuid4(),
                user_id=user.id,
                content_id=content_item.id,
                is_completed=True,
                score=random.uniform(70, 100) if content_item.content_type in ["assessment", "quiz", "exercise"] else None,
                time_spent=random.randint(5, 30) * 60,  # 5-30 minutes in seconds
                last_interaction=completion_time
            )
            
            db.add(ucp)
            completed_count += 1
            
            # Remove this content item from further consideration
            all_content_items.remove(content_item)
    
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
    
    # Make sure we have at least some lessons completed in the last 7 days
    # for the activity graph
    days_ago_list = list(range(7))
    random.shuffle(days_ago_list)
    
    # Mark some lessons as completed
    for i, lesson in enumerate(lessons):
        if i < num_lessons_to_complete:
            # For lessons considered "completed" within this in-progress course
            
            # Ensure some lessons are completed in the last 7 days (for activity graph)
            if i < min(7, num_lessons_to_complete):
                # Use one of the shuffled day offsets to ensure distribution
                day_offset = days_ago_list[i % len(days_ago_list)]
                # Add some hour variation
                completed_at = datetime.now(timezone.utc) - timedelta(
                    days=day_offset,
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
            else:
                # Any remaining lessons can be completed at random times (older)
                completed_at = datetime.now(timezone.utc) - timedelta(
                    days=random.randint(8, 20),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
            
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
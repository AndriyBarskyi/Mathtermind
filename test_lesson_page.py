import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from src.ui.lesson_win import LessonDetailPage
from src.services.course_service import Course

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Lesson Page")
        self.setGeometry(100, 100, 1000, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Create the lesson detail page
        self.lesson_page = LessonDetailPage()
        main_layout.addWidget(self.lesson_page)
        
        # Set the main widget
        self.setCentralWidget(main_widget)
        
        # Add mock courses
        self.add_mock_courses()
    
    def add_mock_courses(self):
        """Add mock courses to the lesson page"""
        logger.info("Adding mock courses")
        
        # Create mock courses
        courses = [
            Course(
                id="course1",
                name="Working with AI",
                description="Learn to work with AI",
                topic="AI",
                difficulty_level="Beginner",
                estimated_duration=60,
                prerequisites=[],
            ),
            Course(
                id="course2",
                name="Business Analytics",
                description="Learn business analytics",
                topic="Analytics",
                difficulty_level="Intermediate",
                estimated_duration=90,
                prerequisites=[],
            ),
            Course(
                id="course3",
                name="Google AI Essentials",
                description="Learn Google AI essentials",
                topic="AI",
                difficulty_level="Beginner",
                estimated_duration=45,
                prerequisites=[],
            ),
            Course(
                id="course4",
                name="IBM Data Analyst",
                description="Learn IBM data analysis",
                topic="Data Science",
                difficulty_level="Advanced",
                estimated_duration=120,
                prerequisites=[],
            ),
            Course(
                id="course5",
                name="Business Analytics with Excel: Elementary to Advanced",
                description="Learn Excel for business analytics",
                topic="Analytics",
                difficulty_level="All Levels",
                estimated_duration=180,
                prerequisites=[],
            ),
            Course(
                id="course6",
                name="Cloud Computing",
                description="Learn cloud computing",
                topic="Cloud",
                difficulty_level="Intermediate",
                estimated_duration=90,
                prerequisites=[],
            ),
        ]
        
        # Update the navigation bar
        logger.info(f"Updating navigation bar with {len(courses)} courses")
        self._update_nav_bar(courses)
    
    def _update_nav_bar(self, courses):
        """Update the navigation bar with course buttons"""
        # Clear existing buttons
        while self.lesson_page.nav_buttons_layout.count():
            item = self.lesson_page.nav_buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add course buttons
        for course in courses:
            logger.info(f"Adding nav button for: {course.name} (ID: {course.id})")
            button = self.lesson_page._create_nav_button(course)
            self.lesson_page.nav_buttons_layout.addWidget(button)
        
        # Add stretch at the end
        self.lesson_page.nav_buttons_layout.addStretch()
        
        # Force update
        self.lesson_page.nav_container.update()
        self.lesson_page.nav_bar.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_()) 
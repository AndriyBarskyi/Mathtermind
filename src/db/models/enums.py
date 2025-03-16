import enum

# TODO: translate all enums to ukrainian

class AgeGroup(str, enum.Enum):
    """Age groups for users."""
    TEN_TO_TWELVE = "10-12"
    THIRTEEN_TO_FOURTEEN = "13-14"
    FIFTEEN_TO_SEVENTEEN = "15-17"

class ContentType(str, enum.Enum):
    """Types of content in the platform."""
    THEORY = "theory"
    EXERCISE = "exercise"
    ASSESSMENT = "assessment"
    INTERACTIVE = "interactive"

class AnswerType(str, enum.Enum):
    """Types of answers for questions."""
    MULTIPLE_CHOICE = "multiple_choice"
    OPEN_ENDED = "open_ended"
    CODE = "code"
    MATHEMATICAL = "mathematical"
    MATCHING = "matching"
    TRUE_FALSE = "true_false"

class InteractiveType(str, enum.Enum):
    """Types of interactive content."""
    SIMULATION = "simulation"
    TOOL = "tool"
    GAME = "game"
    VISUALIZATION = "visualization"

class MathToolType(str, enum.Enum):
    """Types of mathematical tools."""
    CALCULATOR = "calculator"
    GRAPHING = "graphing"
    GEOMETRY = "geometry"
    EQUATION_SOLVER = "equation_solver"
    STATISTICS = "statistics"
    PROBABILITY = "probability"
    MATRIX = "matrix"

class InformaticsToolType(str, enum.Enum):
    """Types of informatics tools."""
    CODE_EDITOR = "code_editor"
    ALGORITHM_VISUALIZER = "algorithm_visualizer"
    DATA_STRUCTURE_VISUALIZER = "data_structure_visualizer"
    LOGIC_CIRCUIT = "logic_circuit"
    DATABASE_DESIGNER = "database_designer"
    NETWORK_SIMULATOR = "network_simulator"

class MetricType(str, enum.Enum):
    """Types of metrics for personal bests."""
    SCORE = "score"
    TIME = "time"
    STREAK = "streak"
    ACCURACY = "accuracy"
    PROBLEMS_SOLVED = "problems_solved"
    CONSECUTIVE_CORRECT = "consecutive_correct"

class Category(str, enum.Enum):
    """Categories for tags."""
    TOPIC = "topic"
    SKILL = "skill"
    DIFFICULTY = "difficulty"
    AGE = "age"
    OTHER = "other"

class ResourceType(str, enum.Enum):
    """Types of resources."""
    VIDEO = "video"
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    LINK = "link"

class Topic(str, enum.Enum):
    """Topics for courses."""
    INFORMATICS = "Informatics"
    MATHEMATICS = "Math"

class DifficultyLevel(str, enum.Enum):
    """Difficulty levels for lessons."""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

class LessonType(str, enum.Enum):
    """Types of lessons."""
    THEORY = "Theory"
    EXERCISE = "Exercise"
    ASSESSMENT = "Assessment"
    INTERACTIVE = "Interactive"

class ThemeType(str, enum.Enum):
    """User interface theme options."""
    LIGHT = "light"
    DARK = "dark"

class FontSize(str, enum.Enum):
    """Font size options for accessibility."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class PreferredSubject(str, enum.Enum):
    """User's preferred subject for study."""
    MATH = "Math"
    INFORMATICS = "Informatics"

class NotificationType(str, enum.Enum):
    """Types of notifications in the system."""
    ACHIEVEMENT = "Achievement"
    COURSE = "Course"
    REMINDER = "Reminder"
    SYSTEM = "System"
    
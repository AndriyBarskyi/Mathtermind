"""
Tag model for the UI.

This module contains the Tag and TagCategory classes used in the UI layer
of the Mathtermind application.
"""

from enum import Enum, auto
from typing import Optional

from pydantic import BaseModel, Field


class TagCategory(str, Enum):
    """Enum for tag categories in the UI."""
    TOPIC = "topic"
    SKILL = "skill"
    DIFFICULTY = "difficulty"
    AGE = "age"
    OTHER = "other"
    
    @classmethod
    def from_db_category(cls, db_category):
        """Convert a database category to a UI category."""
        # Map the DB enum values to UI enum values
        mapping = {
            "TOPIC": cls.TOPIC,
            "SKILL": cls.SKILL,
            "DIFFICULTY": cls.DIFFICULTY,
            "AGE": cls.AGE,
            "OTHER": cls.OTHER
        }
        try:
            # Try to use the enum name (e.g., Category.TOPIC → "TOPIC")
            return mapping.get(db_category.name, cls.OTHER)
        except AttributeError:
            # If db_category is a string, use it directly
            return mapping.get(db_category, cls.OTHER)


class Tag(BaseModel):
    """Tag model for the UI."""
    id: str
    name: str
    category: TagCategory
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            TagCategory: lambda v: v.value
        } 
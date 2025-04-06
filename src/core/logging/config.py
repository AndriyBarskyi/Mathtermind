"""
Logging Configuration Module

This module provides configuration settings for the Mathtermind logging system.
It includes functions to configure the logging system based on application settings.
"""

import os
import logging
from typing import Dict, Any, Optional
from .logger import logger_manager, get_app_logger

# Default log levels for different environments
LOG_LEVELS = {
    "development": {
        "console": logging.DEBUG,
        "file": logging.DEBUG
    },
    "testing": {
        "console": logging.INFO,
        "file": logging.DEBUG
    },
    "production": {
        "console": logging.WARNING,
        "file": logging.INFO
    }
}

# Component-specific log levels
COMPONENT_LOG_LEVELS = {
    "db": {
        "console": logging.INFO,
        "file": logging.DEBUG
    },
    "ui": {
        "console": logging.INFO,
        "file": logging.INFO
    },
    "auth": {
        "console": logging.INFO,
        "file": logging.DEBUG
    }
}


def configure_logging(environment: str = None, config: Dict[str, Any] = None) -> None:
    """
    Configure the logging system based on the application environment and config.
    
    Args:
        environment: The application environment (development, testing, production)
        config: Additional configuration options
    """
    # Use development as default environment
    if environment is None:
        environment = os.getenv("MATHTERMIND_ENV", "development")
    
    # Get appropriate log levels for the environment
    env_levels = LOG_LEVELS.get(environment, LOG_LEVELS["development"])
    
    # Initialize the logger manager with environment-specific settings
    app_logger = get_app_logger()
    
    # Log startup information
    app_logger.info(f"Initializing logging system in {environment} environment")
    
    # Configure component-specific loggers
    for component, levels in COMPONENT_LOG_LEVELS.items():
        component_name = f"mathtermind.{component}"
        console_level = levels.get("console", env_levels["console"])
        file_level = levels.get("file", env_levels["file"])
        
        logger = logger_manager.get_logger(
            component_name,
            console_level=console_level,
            file_level=file_level,
            add_component_file=True
        )
        
        app_logger.debug(f"Configured {component} logger with console={logging.getLevelName(console_level)}, file={logging.getLevelName(file_level)}")
    
    # Add error file handler to the application logger
    logger_manager.add_error_file_handler("mathtermind")
    
    # Add daily rotating handler for important components
    logger_manager.add_daily_rotating_handler("mathtermind", "application_daily.log")
    logger_manager.add_daily_rotating_handler("mathtermind.db", "database_daily.log")
    
    app_logger.info("Logging system initialized successfully")


def update_log_levels(levels: Dict[str, Dict[str, int]]) -> None:
    """
    Update log levels for specific loggers.
    
    Args:
        levels: Dictionary mapping logger names to their console and file log levels
    """
    app_logger = get_app_logger()
    app_logger.info("Updating log levels")
    
    for logger_name, level_dict in levels.items():
        full_name = logger_name if logger_name.startswith("mathtermind") else f"mathtermind.{logger_name}"
        
        if full_name in logger_manager._loggers:
            logger = logger_manager._loggers[full_name]
            
            # Update handler levels
            for handler in logger.handlers:
                if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                    if "console" in level_dict:
                        handler.setLevel(level_dict["console"])
                        app_logger.debug(f"Updated {full_name} console level to {logging.getLevelName(level_dict['console'])}")
                elif isinstance(handler, logging.FileHandler):
                    if "file" in level_dict:
                        handler.setLevel(level_dict["file"])
                        app_logger.debug(f"Updated {full_name} file level to {logging.getLevelName(level_dict['file'])}")
        else:
            app_logger.warning(f"Attempted to update log levels for unknown logger: {full_name}")


def enable_debug_mode() -> None:
    """Enable debug mode for all loggers."""
    get_app_logger().info("Enabling debug mode for all loggers")
    update_log_levels({
        "mathtermind": {"console": logging.DEBUG, "file": logging.DEBUG},
        "mathtermind.db": {"console": logging.DEBUG, "file": logging.DEBUG},
        "mathtermind.ui": {"console": logging.DEBUG, "file": logging.DEBUG},
    }) 
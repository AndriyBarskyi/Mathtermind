"""
Mathtermind Application Initialization

This module handles the initialization of the Mathtermind application,
including setting up logging, error handling, database connections,
and other application-wide configurations.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Import our logging and error handling framework
from src.core import initialize as init_core, get_logger
from src.core.error_handling import (
    ConfigurationError, 
    DatabaseConnectionError,
    create_error_boundary,
    report_error
)

# Set up logging
logger = get_logger(__name__)


def init_app(environment: str = None, config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Initialize the Mathtermind application.
    
    Args:
        environment: The environment to run in (development, testing, production)
        config_path: Path to a custom configuration file
        
    Returns:
        Application configuration dictionary
    """
    # Initialize the core framework (logging and error handling)
    init_core(environment)
    
    # Log application startup
    logger.info("Initializing Mathtermind application")
    logger.info(f"Running in {environment or 'development'} environment")
    
    # Load configuration
    config = load_config(environment, config_path)
    
    # Initialize components
    with create_error_boundary("database_initialization"):
        init_database(config)
    
    with create_error_boundary("services_initialization"):
        init_services(config)
    
    logger.info("Application initialization completed successfully")
    return config


def load_config(environment: str = None, config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load application configuration.
    
    Args:
        environment: The environment to load configuration for
        config_path: Path to a custom configuration file
        
    Returns:
        Configuration dictionary
    """
    logger.info("Loading application configuration")
    
    try:
        # Default configuration
        config = {
            "environment": environment or os.getenv("MATHTERMIND_ENV", "development"),
            "debug": os.getenv("DEBUG_MODE", "True").lower() == "true",
            "database_url": os.getenv("DATABASE_URL", "sqlite:///mathtermind.db"),
            "data_dir": "data",
            "log_dir": "logs",
        }
        
        # Load environment-specific configuration
        env = config["environment"]
        logger.debug(f"Loading configuration for {env} environment")
        
        if env == "development":
            config.update({
                "debug": True,
                "auto_reload": True,
            })
        elif env == "testing":
            config.update({
                "debug": True,
                "database_url": "sqlite:///mathtermind_test.db",
                "auto_reload": False,
            })
        elif env == "production":
            config.update({
                "debug": False,
                "auto_reload": False,
            })
        
        # Load custom configuration if provided
        if config_path:
            logger.debug(f"Loading custom configuration from {config_path}")
            
            try:
                import json
                with open(config_path, 'r') as f:
                    custom_config = json.load(f)
                
                config.update(custom_config)
                logger.info(f"Loaded custom configuration from {config_path}")
            except Exception as e:
                logger.error(f"Failed to load custom configuration: {str(e)}")
                raise ConfigurationError(
                    message=f"Failed to load custom configuration from {config_path}",
                    config_key="custom_config",
                    details={"error": str(e), "path": config_path}
                ) from e
        
        logger.info("Configuration loaded successfully")
        return config
        
    except Exception as e:
        logger.error(f"Configuration loading failed: {str(e)}")
        report_error(e, operation="load_config", environment=environment)
        raise ConfigurationError(
            message="Failed to load application configuration",
            details={"error": str(e), "environment": environment}
        ) from e


def init_database(config: Dict[str, Any]) -> None:
    """
    Initialize database connections and ORM.
    
    Args:
        config: Application configuration
    """
    logger.info("Initializing database connection")
    
    try:
        from src.db import init_db, engine
        
        # Initialize the database if it doesn't exist
        data_dir = config.get("data_dir", "data")
        os.makedirs(data_dir, exist_ok=True)
        
        # Check database connection
        try:
            # Try to connect to the database
            connection = engine.connect()
            connection.close()
            logger.info("Database connection established successfully")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise DatabaseConnectionError(
                message="Failed to connect to the database",
                details={"error": str(e), "database_url": config.get("database_url")}
            ) from e
            
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        report_error(e, operation="init_database", config=config)
        raise


def init_services(config: Dict[str, Any]) -> None:
    """
    Initialize application services.
    
    Args:
        config: Application configuration
    """
    logger.info("Initializing application services")
    
    try:
        # Import and initialize services
        from src.services import init_services as init_svc
        
        init_svc(config)
        logger.info("Services initialized successfully")
        
    except Exception as e:
        logger.error(f"Service initialization failed: {str(e)}")
        report_error(e, operation="init_services", config=config)
        raise


if __name__ == "__main__":
    """
    Command-line interface for application initialization.
    
    Usage:
        python -m src.app_init [environment] [--config=CONFIG_PATH]
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize Mathtermind application")
    parser.add_argument("environment", nargs="?", default=None, 
                        help="Environment to run in (development, testing, production)")
    parser.add_argument("--config", dest="config_path", default=None,
                        help="Path to custom configuration file")
    parser.add_argument("--debug", action="store_true", 
                        help="Enable debug logging")
    
    args = parser.parse_args()
    
    # Enable debug mode if requested
    if args.debug:
        from src.core import debug_mode
        debug_mode()
    
    try:
        # Initialize the application
        config = init_app(args.environment, args.config_path)
        print(f"Application initialized successfully in {config['environment']} environment")
        sys.exit(0)
    except Exception as e:
        print(f"Application initialization failed: {str(e)}")
        sys.exit(1) 
#!/usr/bin/env python3
"""
Database Management Script

This script provides a command-line interface for managing the Mathtermind database.
It handles migrations, seeding, and other database operations.

Usage:
    python db_manage.py init      - Initialize the database with the latest schema
    python db_manage.py migrate   - Run all pending migrations
    python db_manage.py seed      - Seed the database with sample data
    python db_manage.py reset     - Reset the database (drop all tables and recreate)
    python db_manage.py status    - Show the current migration status
    python db_manage.py create_migration "message" - Create a new migration
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from config import DATABASE_PATH, DATA_DIR
from src.db import engine
from src.db.models.base import Base


def run_alembic_command(command, *args):
    """Run an Alembic command with the given arguments."""
    alembic_dir = project_root / "src" / "db"
    cmd = ["python", "-m", "alembic", command]
    cmd.extend(args)
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=alembic_dir)
    return result.returncode


def init_db():
    """Initialize the database with the latest schema."""
    print(f"Initializing database at {DATABASE_PATH}...")
    
    # Create the data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Create all tables
    Base.metadata.create_all(engine)
    print("Database schema created successfully.")
    
    # Stamp the database with the current migration version
    run_alembic_command("stamp", "head")
    print("Database stamped with the current migration version.")


def migrate_db():
    """Run all pending migrations."""
    print("Running database migrations...")
    return run_alembic_command("upgrade", "head")


def seed_db():
    """Seed the database with sample data."""
    print("Seeding the database with sample data...")
    
    # Import and run the seed scripts
    from src.db.seed_users import seed_users
    from src.db.seed_courses import seed_courses
    
    seed_users()
    seed_courses()
    
    print("Database seeding completed successfully.")


def reset_db():
    """Reset the database (drop all tables and recreate)."""
    print(f"Resetting database at {DATABASE_PATH}...")
    
    # Drop all tables
    Base.metadata.drop_all(engine)
    print("All tables dropped.")
    
    # Create all tables
    Base.metadata.create_all(engine)
    print("Database schema recreated successfully.")
    
    # Stamp the database with the current migration version
    run_alembic_command("stamp", "head")
    print("Database stamped with the current migration version.")


def show_status():
    """Show the current migration status."""
    print("Current database migration status:")
    return run_alembic_command("current")


def create_migration(message):
    """Create a new migration."""
    print(f"Creating new migration: {message}")
    return run_alembic_command("revision", "--autogenerate", "-m", message)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Mathtermind Database Management")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Init command
    subparsers.add_parser("init", help="Initialize the database with the latest schema")
    
    # Migrate command
    subparsers.add_parser("migrate", help="Run all pending migrations")
    
    # Seed command
    subparsers.add_parser("seed", help="Seed the database with sample data")
    
    # Reset command
    subparsers.add_parser("reset", help="Reset the database (drop all tables and recreate)")
    
    # Status command
    subparsers.add_parser("status", help="Show the current migration status")
    
    # Create migration command
    create_parser = subparsers.add_parser("create_migration", help="Create a new migration")
    create_parser.add_argument("message", help="Migration message")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_db()
    elif args.command == "migrate":
        migrate_db()
    elif args.command == "seed":
        seed_db()
    elif args.command == "reset":
        reset_db()
    elif args.command == "status":
        show_status()
    elif args.command == "create_migration":
        create_migration(args.message)
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 
# Database Management in Mathtermind

This document describes the database management approach used in the Mathtermind project.

## Database Structure

- **Database Type**: SQLite
- **Database Location**: `data/mathtermind.db`
- **Schema Management**: Alembic migrations
- **Models**: SQLAlchemy ORM models in `src/db/models/`

## Database Management Tool

The project includes a database management tool (`db_manage.py`) that provides a command-line interface for common database operations:

```bash
# Initialize the database with the latest schema
python db_manage.py init

# Run all pending migrations
python db_manage.py migrate

# Seed the database with sample data
python db_manage.py seed

# Reset the database (drop all tables and recreate)
python db_manage.py reset

# Show the current migration status
python db_manage.py status

# Create a new migration
python db_manage.py create_migration "Description of changes"
```

## Migrations with Alembic

Alembic is used for database migrations. The migration files are stored in `src/db/migrations/versions/`.

### Migration Workflow

1. **Make changes to your models** in `src/db/models/`.
2. **Create a new migration**:
   ```bash
   python db_manage.py create_migration "Description of changes"
   ```
3. **Review the generated migration** in `src/db/migrations/versions/`.
4. **Apply the migration**:
   ```bash
   python db_manage.py migrate
   ```

### SQLite Limitations

SQLite has limitations when it comes to ALTER TABLE operations. The Alembic environment has been configured to handle these limitations by using batch operations for SQLite.

## Data Seeding

The project includes scripts for seeding the database with sample data:

- `src/db/seed_users.py`: Creates sample users
- `src/db/seed_courses.py`: Creates sample courses and lessons

These scripts are called by the `db_manage.py seed` command.

## Best Practices

1. **Always use migrations** for schema changes.
2. **Test migrations** in development before applying them to production.
3. **Keep migration files small** and focused on specific changes.
4. **Document complex migrations** with comments.
5. **Use the database management tool** for all database operations.
6. **Never modify the database schema manually**.

## Troubleshooting

### Multiple Heads

If you encounter a "Multiple heads" error when running migrations, you need to merge the heads:

```bash
cd src/db
python -m alembic merge heads -m "Merge heads"
python -m alembic upgrade head
```

### Migration Conflicts

If a migration fails due to conflicts with the existing database schema, you may need to:

1. Reset the database (if in development):
   ```bash
   python db_manage.py reset
   ```

2. Or create a new migration that handles the conflicts:
   ```bash
   python db_manage.py create_migration "Fix conflicts"
   ```
   Then edit the migration file manually to handle the conflicts. 
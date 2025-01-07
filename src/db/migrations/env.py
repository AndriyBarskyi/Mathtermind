from db.base import Base
from db.session import engine
target_metadata = Base.metadata

def run_migrations_online():
    from alembic import context
    connectable = engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
run_migrations_online()

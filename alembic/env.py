from logging.config import fileConfig
import sys
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from alembic import context

# -------------------------------------------------
# FIX IMPORT PATH (CRITICAL FOR WINDOWS)
# -------------------------------------------------
sys.path.append(str(Path(__file__).resolve().parents[1]))

# -------------------------------------------------
# ALEMBIC CONFIG
# -------------------------------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -------------------------------------------------
# IMPORT SQLMODEL + ALL MODELS
# -------------------------------------------------
from sqlmodel import SQLModel

from app.models.user import User
from app.models.attendance import Attendance
from app.models.leave import LeaveRequest
from app.models.payroll import Payroll

target_metadata = SQLModel.metadata

# -------------------------------------------------
# OFFLINE MIGRATIONS
# -------------------------------------------------
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# -------------------------------------------------
# ONLINE MIGRATIONS
# -------------------------------------------------
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# -------------------------------------------------
# ENTRYPOINT
# -------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

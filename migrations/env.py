import sys
import os
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

# from app.common.config import settings
# from app.common.config import log_settings
from app.common.database import Base
from loguru import logger

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# log_settings("env.py --->", settings)

# Alembic Config object
config = context.config

# Set up logging from alembic.ini
# fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate' support
target_metadata = Base.metadata

# Set the SQLAlchemy URL dynamically from Dynaconf settings
# config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# with this, the schema generation works (alembic upgrade head)
# config.set_main_option(
#     "sqlalchemy.url", "postgresql://postgres:123456@localhost:5433/metadata_service_2"
# )


def run_migrations_offline():
    logger.debug("running Migration offline")
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    logger.debug("running Migration ONLINE")
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


# import sys
# import os
#
# from app.common.config import settings
# from app.common.database import Base
#
# # Add the project root to sys.path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
# from alembic import context
# from sqlalchemy import engine_from_config, pool
# from logging.config import fileConfig
#
# from loguru import logger
# settings.get("lkjlk")
#
# # Alembic Config object
# config = context.config
#
# # Set up logging from alembic.ini
# fileConfig(config.config_file_name)
#
# # Set target metadata for 'autogenerate' support
# target_metadata = Base.metadata
#
# def run_migrations_offline():
#     logger.debug("running Migration offline")
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
#     )
#
#     with context.begin_transaction():
#         context.run_migrations()
#
# def run_migrations_online():
#     logger.debug("running Migration ONLINE")
#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )
#
#     with connectable.connect() as connection:
#         context.configure(connection=connection, target_metadata=target_metadata)
#
#         with context.begin_transaction():
#             context.run_migrations()
#
# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()

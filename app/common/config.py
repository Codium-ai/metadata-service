"""

Configuration settings for the application.

# Precedence of settings:
# -----------------------
# environment variables
# .env file (if load_dotenv=True)
# settings_files (taking into consideration only settings for the correct env

"""

import json

from dynaconf import Dynaconf
from loguru import logger

settings = Dynaconf(
    settings_files=[
        "config/settings.toml",
        "config/settings.dev.toml",
        "config/settings.test.toml",
        "config/settings.prod.toml",
        "config/.secrets.toml",
    ],
    env_switcher="ENV_FOR_DYNACONF",
    environments=True,
    load_dotenv=True,
)


def get_connection_url():
    user = settings.database_user
    password = settings.database_password
    name = settings.database_name
    host = settings.database_host
    port = settings.database_port

    # Construct and return the connection URL
    connection_url = f"postgresql://{user}:{password}@{host}:{port}/{name}"
    # "postgresql://postgres:123456@localhost:5433/metadata_service"
    return connection_url


# settings.DATABASE_URL = get_connection_url()
settings.DATABASE_URL = "postgresql://postgres:123456@localhost:5433/metadata_service_2"

#"postgresql://postgres:123456@localhost:5433/metadata_service_2_kuku"
def log_settings(prefix, settings_obj):
    # Convert settings to dictionary
    settings_dict = settings_obj.as_dict()

    # Convert dictionary to JSON string
    settings_json = json.dumps(settings_dict, indent=2)
    logger.debug(f"{prefix} Settings: {settings_json}")
    logger.debug(
        f"{prefix} SETTINGS_FILE_FOR_DYNACONF: {settings_obj.SETTINGS_FILE_FOR_DYNACONF}"
    )

"""Application configurations, mostly sourced from an environment file

Configurations should be represented in the Settings class so they can be
reused easily throughout the code
"""

import typing

import databases
from pydantic import AnyUrl, BaseSettings, ValidationError, root_validator

__all__ = ["settings"]


class Settings(BaseSettings):

    ENVIRONMENT: str
    OUTPOST_MODE: bool

    OUTPOST_DB_NAME: str
    OUTPOST_DB_HOST: str  # should be a url type but this sometimes has errors
    OUTPOST_DB_PORT: int
    OUTPOST_DB_USER: str
    OUTPOST_DB_PASSWORD: str
    OUTPOST_DB_DRIVER: str

    LEADER_DB_NAME: str
    LEADER_DB_HOST: str  # should be a url type but this sometimes has errors
    LEADER_DB_PORT: int
    LEADER_DB_USER: str
    LEADER_DB_PASSWORD: str
    LEADER_DB_DRIVER: str

    LEADER_DB: typing.Optional[databases.Database] = None
    OUTPOST_DB: typing.Optional[databases.Database] = None

    @root_validator
    def configure_databases(cls, values):
        """Instantiates leader and outpost db and sets them as configuration values"""
        try:
            _LEADER_DB_DRIVER = values["LEADER_DB_DRIVER"]
            _LEADER_DB_USER = values["LEADER_DB_USER"]
            _LEADER_DB_PASSWORD = values["LEADER_DB_PASSWORD"]
            _LEADER_DB_HOST = values["LEADER_DB_PASSWORD"]
            _LEADER_DB_PORT = values["LEADER_DB_PORT"]
            _LEADER_DB_NAME = values["LEADER_DB_NAME"]

            _OUTPOST_DB_DRIVER = values["OUTPOST_DB_DRIVER"]
            _OUTPOST_DB_USER = values["OUTPOST_DB_USER"]
            _OUTPOST_DB_PASSWORD = values["OUTPOST_DB_PASSWORD"]
            _OUTPOST_DB_HOST = values["OUTPOST_DB_PASSWORD"]
            _OUTPOST_DB_PORT = values["OUTPOST_DB_PORT"]
            _OUTPOST_DB_NAME = values["OUTPOST_DB_NAME"]
            _OUTPOST_MODE = values["OUTPOST_MODE"]
        except KeyError as e:
            raise ValueError(f"{e} is missing from env variables")

        leader_db_connection_string = f"{_LEADER_DB_DRIVER}://{_LEADER_DB_USER}:{_LEADER_DB_PASSWORD}@{_LEADER_DB_HOST}:{_LEADER_DB_PORT}/{_LEADER_DB_NAME}"
        outpost_db_connection_string = f"{_OUTPOST_DB_DRIVER}://{_OUTPOST_DB_USER}:{_OUTPOST_DB_PASSWORD}@{_OUTPOST_DB_HOST}:{_OUTPOST_DB_PORT}/{_OUTPOST_DB_NAME}"

        if isinstance(_OUTPOST_MODE, str):
            # Just a double check to ensure that the outpost mode configuration
            # is always accurate
            _OUTPOST_MODE = True if _OUTPOST_MODE == "True" else False

        # Import checks to ensure that there are no errors with setting outpost mode
        if (
            not _OUTPOST_MODE
            and leader_db_connection_string != outpost_db_connection_string
        ):
            raise ValueError(
                "App is in outpost mode but leader and outpost db are not matching!"
            )
        if (
            _OUTPOST_MODE
            and leader_db_connection_string == outpost_db_connection_string
        ):
            raise ValueError(
                "App is in outpost mode but leader and outpost db are matching!"
            )

        values["LEADER_DB"] = databases.Database(leader_db_connection_string)
        if _OUTPOST_MODE:
            values["OUTPOST_DB"] = databases.Database(
                outpost_db_connection_string
            )
        else:
            # set them to the same object. Helpful in testing
            values["OUTPOST_DB"] = values["LEADER_DB"]
        return values

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        arbitrary_types_allowed = True


settings = Settings()

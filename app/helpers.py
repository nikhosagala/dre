from os import getenv


def get_env(env_name: str, default: str):
    value = getenv(env_name)

    if not value:
        return default

    return value

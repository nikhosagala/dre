from functools import partial
from os import getenv
from typing import Callable


def get_env(env_name: str, default: str, type: Callable[[str], any] = str) -> any:
    value = getenv(env_name)

    if not value:
        return default

    return type(value)


_str = partial(get_env, type=str)


def _bool(varname: str, default: bool = None) -> bool:
    return get_env(varname, default, lambda x: x.lower() in ['1', 'true', 't'])


def _int(varname: str, default: int = None) -> int:
    return get_env(varname, default, int)


class EnvConfig:

    def boolean(self, varname: str, default: bool = None) -> bool:
        return _bool(varname, default)

    def string(self, varname: str, default: str = None) -> str:
        return _str(varname, default)

    def int(self, varname: str, default: int = None) -> int:
        return _int(varname, default)

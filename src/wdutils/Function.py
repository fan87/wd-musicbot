from types import CodeType
from typing import Any


class Function:
    __name__: str = ""
    __module__: str = ""
    __code__: CodeType = None
    __qualname__: str = ""
    __annotations__: dict = {}

    def __call__(self, *args, **kwargs):
        pass

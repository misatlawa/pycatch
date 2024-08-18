from types import TracebackType
from typing import Protocol, Type


class ExceptionHandler(Protocol):
    def __call__(self, exc_type: Type[Exception], exc_val: str, exc_tb: TracebackType): ...


def raise_(exc_type: Type[Exception], exc_val: str, exc_tb: TracebackType):
    raise exc_type(exc_val).with_traceback(exc_tb)


def pass_(exc_type: Type[Exception], exc_val: str, exc_tb: TracebackType):
    pass


import inspect
from functools import wraps
from types import FrameType
from typing import Type, Any, Callable, TypeVar, List

from pycatch import UncheckedExceptionError


_CHECK_EXCEPTIONS = True
_REQUIRE_UNBROKEN_CHAIN = True


def check_exceptions(b: bool):
    global _CHECK_EXCEPTIONS
    _CHECK_EXCEPTIONS = b


def require_unbroken_chain(b: bool):
    global _REQUIRE_UNBROKEN_CHAIN
    _REQUIRE_UNBROKEN_CHAIN = b


def _get_catches(frame: FrameType) ->  List[Type[Exception]]:
    catches = frame.f_locals.get('__catches__', tuple())
    if not catches and not _REQUIRE_UNBROKEN_CHAIN:
        while frame and not catches:
            catches = frame.f_locals.get('__catches__', tuple())
            frame = frame.f_back

    return catches


def _get_previous_throws(frame: FrameType) -> List[Type[Exception]]:
    frame = frame.f_back
    previous_throws = frame.f_locals.get('__throws__', tuple())
    if not previous_throws and not _REQUIRE_UNBROKEN_CHAIN:
        while frame and not previous_throws:
            previous_throws = frame.f_locals.get('__throws__', tuple())
            frame = frame.f_back

    return previous_throws


_F = TypeVar("_F", bound=Callable[..., Any])

def throws(*exc_types: Type[Exception]) -> Callable[[_F], _F]:
    def wrap(f: _F) -> _F:
        if not _CHECK_EXCEPTIONS:
            return f

        @wraps(f)
        def call(*args, **kwargs):
            frame = inspect.stack()[1].frame
            caller_throws = _get_previous_throws(frame)
            caller_catches = _get_catches(frame)
            __catches__ = (*caller_throws, *caller_catches)
            __throws__ =  (*caller_throws, *exc_types)

            for exc_type in exc_types:
                if exc_type not in __catches__:
                    raise UncheckedExceptionError(exc_type.__name__)

            return f(*args, **kwargs)
        return call
    return wrap

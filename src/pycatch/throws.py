
import inspect
from functools import wraps
from typing import Type, Dict, Any, Callable

from pycatch import UncheckedExceptionError


def _check_caller_catches_exc(exc_type: Type[Exception], caller_locals: Dict[str, Any]) -> bool:
    return '__catches__' in caller_locals and exc_type in caller_locals['__catches__']


def _check_caller_throws_exc(exc_type: Type[Exception], caller_caller_locals: Dict[str, Any]):
    caller_is_decorated = caller_caller_locals.get('__is_throws_decorator__')
    return caller_is_decorated and exc_type in caller_caller_locals['__throws__']


def throws(exc_type: Type[Exception]):
    def wrap(f: Callable) -> Callable:
        @wraps(f)
        def call(*args, **kwargs):
            caller_frame = inspect.stack()[1].frame
            caller_locals = caller_frame.f_locals
            if caller_frame.f_back is None:
                caller_caller_locals = dict()
            else:
                caller_caller_locals = caller_frame.f_back.f_locals

            caller_caches_exc = _check_caller_catches_exc(exc_type, caller_locals)
            caller_throws_exc = _check_caller_throws_exc(exc_type, caller_caller_locals)

            __is_throws_decorator__ = True
            __catches__ = list()
            __throws__ = [exc_type]

            if caller_caches_exc:
                __catches__ = caller_locals['__catches__']

                # chaining multiple `throws` decorators sums theirs lists of thrown exceptions
                if caller_locals.get('__is_throws_decorator__'):
                    __throws__ += caller_locals['__throws__']

            elif caller_throws_exc:
                __catches__ = caller_caller_locals['__throws__']

            else:
                raise UncheckedExceptionError(exc_type.__name__)

            return f(*args, **kwargs)
        return call
    return wrap

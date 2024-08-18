
import inspect
import types
from typing import Type, Optional

from pycatch.handlers import raise_, ExceptionHandler


class Catch:
	def __init__(self, *exc_types: Type[Exception], handler: ExceptionHandler = raise_):
		self._exc_types = exc_types
		self._handler = handler
		self._catches_before = list()

	def __enter__(self):
		this_frame = inspect.stack()[1].frame
		caller_frame = this_frame.f_back
		caller_frame_throws = (caller_frame and caller_frame.f_locals.get('__throws__')) or tuple()
		self._catches_before = this_frame.f_locals.get('__catches__') or tuple()
		this_frame.f_locals['__catches__'] = (*self._exc_types, *self._catches_before, *caller_frame_throws)

		return self

	def __exit__(self,
	             exc_type: Optional[Type[Exception]],
	             exc_val: Optional[str],
	             exc_tb: types.TracebackType) -> bool:
		this_frame = inspect.stack()[1].frame
		this_frame.f_locals['__catches__'] = self._catches_before
		if exc_type is not None and exc_val is not None and exc_tb is not None:
			if exc_type in self._exc_types:
				self._handler(exc_type, exc_val, exc_tb)
				return True
		return False

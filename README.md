## PyCatch ##

PyCatch allows Java-like exception declarations for python methods.
Introduces `throws` decorator and `Catch` context manager and raises
`UncheckedExceptionError` if declared exception is not handled.

## Usage ##

```python
from pycatch import throws

@throws(ZeroDivisionError)
def divide(x, y):
    return x / y

divide(3, 2) # raises UncheckedExceptionError: ZeroDivisionError 
```

```python
from pycatch import Catch, throws

@throws(ZeroDivisionError)
def divide(x, y):
    return x / y

with Catch(ZeroDivisionError):
    divide(3, 2) # no exceptions
```

```python
from pycatch import Catch, handlers, throws

@throws(ZeroDivisionError)
def divide(x, y):
    return x / y

with Catch(ZeroDivisionError, handler=handlers.pass_):
    divide(3, 0) # still no exceptions
```
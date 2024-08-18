import pytest

from pycatch import throws, Catch
from pycatch.handlers import pass_, raise_


def test_pass():
    @throws(ZeroDivisionError)
    def divide(x, y):
        return x / y

    with Catch(ZeroDivisionError, handler=pass_):
        divide(1, 0)


def test_nested_pass():
    @throws(TypeError)
    @throws(ZeroDivisionError)
    def divide(x, y):
        return x / y

    with Catch(ZeroDivisionError, handler=pass_):
        with Catch(TypeError):
            divide(3, 2)


def test_raise():
    @throws(ZeroDivisionError)
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        with Catch(ZeroDivisionError, handler=raise_):
            divide(1, 0)


def test_nested_raise():
    @throws(TypeError)
    @throws(ZeroDivisionError)
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        with Catch(ZeroDivisionError, handler=raise_):
            with Catch(TypeError):
                divide(1, 0)

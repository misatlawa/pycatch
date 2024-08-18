from typing import Tuple, Type

import pytest

from pycatch import throws, Catch


def test_catch():

    @throws(ZeroDivisionError)
    def divide(x, y):
        return x / y

    with Catch(ZeroDivisionError):
        divide(3, 2)


def test_catch_nested_throws():

    @throws(ZeroDivisionError)
    def divide1(x, y):
        return x / y

    @throws(ZeroDivisionError)
    def divide2(x, y):
        return divide1(x, y)

    with Catch(ZeroDivisionError):
        divide2(3, 2)


@pytest.mark.parametrize('catch_exceptions', [(ZeroDivisionError, TypeError),
                                              (TypeError, ZeroDivisionError)])
@pytest.mark.parametrize('throws_exceptions', [(ZeroDivisionError, TypeError),
                                               (TypeError, ZeroDivisionError)])
def test_catch_multiple_throws(throws_exceptions: Tuple[Type[Exception], Type[Exception]],
                               catch_exceptions: Tuple[Type[Exception], Type[Exception]]):

    @throws(throws_exceptions[0])
    @throws(throws_exceptions[1])
    def divide(x, y):
        return x / y

    with Catch(catch_exceptions[0], catch_exceptions[1]):
        divide(3, 2)


def test_catch_multiple_throws_deep():

    @throws(TypeError, ZeroDivisionError)
    def divide_0(x, y):
        return x / y

    @throws(TypeError, ZeroDivisionError)
    def divide_1(x, y):
        return divide_0(x, y)

    with Catch(ZeroDivisionError, TypeError):
        divide_1(3, 2)


def test_catch_multiple_throws_wide():

    @throws(ZeroDivisionError)
    def divide(x, y):
        return x / y

    @throws(TypeError)
    def invert_divide(x, y):
        return y / x

    @throws(ZeroDivisionError, TypeError)
    def one(x, y):
        return divide(x, y) * invert_divide(x, y)

    with Catch(ZeroDivisionError, TypeError):
        one(3, 2)


@pytest.mark.parametrize('catch_exceptions', [(ZeroDivisionError, TypeError), (TypeError, ZeroDivisionError)])
def test_nested_catch(catch_exceptions: Tuple[Type[Exception], Type[Exception]]):
    @throws(TypeError, ZeroDivisionError)
    def divide(x, y):
        return x / y

    with Catch(catch_exceptions[0]):
        with Catch(catch_exceptions[1]):
            divide(3, 2)


def test_nested_catch_nested_throws():

    @throws(TypeError, ZeroDivisionError)
    def divide1(x, y):
        return x / y

    @throws(ZeroDivisionError)
    def divide2(x, y):
        with Catch(TypeError):
            return divide1(x, y)

    with Catch(ZeroDivisionError):
        divide2(3, 2)


def test_catch_raise_unhandled_exception():
    def divide(x, y):
        raise NotImplementedError("This should not be caught")

    with pytest.raises(NotImplementedError):
        with Catch(ZeroDivisionError):
            divide(3, 2)

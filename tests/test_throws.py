
import pytest

from pycatch import throws, UncheckedExceptionError, Catch, require_unbroken_chain, check_exceptions


def test_throws_no_catch():

    @throws(ZeroDivisionError)
    def divide(x, y):
        return x / y

    with pytest.raises(UncheckedExceptionError):
        divide(3, 2)


def test_throws_multiple_no_catch():

    @throws(ZeroDivisionError)
    @throws(TypeError)
    def divide(x, y):
        return x / y

    with pytest.raises(UncheckedExceptionError):
        divide(3, 2)


def test_throws_multiple_incomplete_catch():

    @throws(TypeError)
    @throws(ZeroDivisionError)
    def divide(x, y):
        return x / y

    with pytest.raises(UncheckedExceptionError):
        with Catch(ZeroDivisionError):
            divide(3, 2)


def test_throws_missing_nested_catch():

    @throws(ZeroDivisionError)
    def divide1(x, y):
        return x / y

    def divide2(x, y):
        return divide1(x, y)

    with pytest.raises(UncheckedExceptionError):
        with Catch(ZeroDivisionError):
            divide2(3, 2)


def test_throws_multiple_missing_nested_catch():

    @throws(TypeError, ZeroDivisionError)
    def divide1(x, y):
        return x / y

    @throws(TypeError)
    def divide2(x, y):
        return divide1(x, y)

    with pytest.raises(UncheckedExceptionError):
        with Catch(ZeroDivisionError, TypeError):
            divide2(3, 2)


def test_throws_before_call():
    @throws(NotImplementedError)
    def divide(x, y):
        raise NotImplementedError("This should not be raised")

    with pytest.raises(UncheckedExceptionError):
        with Catch(ZeroDivisionError):
            divide(3, 2)


def test_throws_on_next_call():
    @throws(ZeroDivisionError)
    def divide(x, y):
        return x / y

    with Catch(ZeroDivisionError):
        divide(3, 2)

    with pytest.raises(UncheckedExceptionError):
        divide(3, 2)

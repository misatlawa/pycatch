
import pytest as pytest
import pycatch


@pytest.fixture
def dont_check_exception():
    pycatch.check_exceptions(False)
    yield
    pycatch.check_exceptions(True)


@pytest.fixture
def dont_require_unbroken_chain():
    pycatch.require_unbroken_chain(False)
    yield
    pycatch.require_unbroken_chain(True)


def test_accepts_no_catch(dont_check_exception):
    @pycatch.throws(ZeroDivisionError)
    def divide(x, y):
        return x / y

    divide(3, 2)


def test_accepts_missing_nested_catch(dont_require_unbroken_chain):
    @pycatch.throws(ZeroDivisionError)
    def divide1(x, y):
        return x / y

    def divide2(x, y):
        return divide1(x, y)

    def divide3(x, y):
        return divide2(x, y)

    with pycatch.Catch(ZeroDivisionError):
        divide3(3, 2)

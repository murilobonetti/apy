import pytest


def raises_error():
    raise SystemExit(1)


def adds_one(x):
    return x + 1


def test_adds_one():
    assert adds_one(4) == 5


def test_mytest():
    with pytest.raises(SystemExit):
        raises_error()

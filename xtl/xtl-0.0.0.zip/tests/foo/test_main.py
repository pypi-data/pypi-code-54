import pytest

from src.xtl.main import add


class TestAdd:
    def test_add_1(self):
        assert add(1, 1) == 2

    def test_add_2(self):
        assert add(1, 2) == 3

    @pytest.mark.xfail(strict=True)
    def test_add_3(self):
        assert add(1, 1) == 1

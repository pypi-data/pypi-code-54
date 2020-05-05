from pathlib import Path

import pytest
from expects import *
from ndd_test4p.test_cases import AbstractTest

from ndd_utils4p.text import TextFileSerializer


class TestTextFileSerializer(AbstractTest):

    @pytest.fixture()
    def template_file_path(self) -> Path:
        return self._test_data_file_path('template.txt.j2')

    @pytest.fixture()
    def serializer(self) -> TextFileSerializer:
        return TextFileSerializer()

    @pytest.fixture()
    def data(self) -> str:
        return 'Some textual data\n'

    def test_load(self, serializer):
        actual_result = serializer.load(self._test_data_file_path('data.txt'))
        expected_result = 'Some textual data\n'
        expect(actual_result).to(equal(expected_result))

    def test_save(self, tmp_path: Path, serializer, data):
        actual_result_path = tmp_path.joinpath('actual_result.txt')
        actual_result = serializer.save(data, actual_result_path)
        expected_result = 'Some textual data\n'
        expect(actual_result_path.read_text()).to(equal(expected_result))
        expect(actual_result).to(equal(expected_result))

    def test_default_extension(self, serializer):
        expect(serializer.default_extension()).to(equal('txt'))

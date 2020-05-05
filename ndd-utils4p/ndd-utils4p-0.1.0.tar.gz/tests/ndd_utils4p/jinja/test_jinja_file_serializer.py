from pathlib import Path
from typing import Dict

import pytest
from expects import *
from ndd_test4p.differences_viewers import TextDifferencesViewer
from ndd_test4p.test_cases import AbstractTest

from ndd_utils4p.jinja import JinjaFileSerializer


class TestJinjaFileSerializer(AbstractTest):

    @pytest.fixture()
    def template_file_path(self) -> Path:
        return self._test_data_file_path('template.txt.j2')

    @pytest.fixture()
    def serializer(self, template_file_path) -> JinjaFileSerializer:
        # return JinjaFileSerializer(JinjaExporter(template_file_path))
        return JinjaFileSerializer.from_template_file(template_file_path)

    @pytest.fixture()
    def data(self) -> Dict:
        return {
            'locations': [
                {'name': 'Seattle', 'state': 'WA'},
                {'name': 'New York', 'state': 'NY'},
                {'name': 'Bellevue', 'state': 'WA'},
                {'name': 'Olympia', 'state': 'WA'}
            ]
        }

    def test_load(self, serializer):
        with pytest.raises(NotImplementedError):
            serializer.load(self._test_data_file_path('expected_result.txt'))

    def test_save(self, tmp_path: Path, serializer, data):
        actual_result_path = tmp_path.joinpath('actual_result.txt')
        actual_result = serializer.save(data, actual_result_path)
        expected_result_path = self._test_data_file_path('expected_result.txt')
        expected_result = self._test_data_from('expected_result.txt')

        with TextDifferencesViewer(actual_result, expected_result_path):
            expect(actual_result_path.read_text()).to(equal(expected_result))
        with TextDifferencesViewer(actual_result, expected_result_path):
            expect(actual_result).to(equal(expected_result))

    def test_default_extension(self, serializer):
        expect(serializer.default_extension()).to(be_none)

from pathlib import Path
from typing import Dict

import pytest
from expects import *
from ndd_test4p.differences_viewers import TextDifferencesViewer
from ndd_test4p.test_cases import AbstractTest

from ndd_utils4p.jinja import JinjaExporter


class TestJinjaExporter(AbstractTest):

    @pytest.fixture()
    def template_file_path(self) -> Path:
        return self._test_data_file_path('template.txt.j2')

    @pytest.fixture()
    def exporter(self, template_file_path) -> JinjaExporter:
        return JinjaExporter(template_file_path)

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

    def test_export(self, exporter, data):
        actual_result = exporter.export(data)
        expected_result_path = self._test_data_file_path('expected_result.txt')
        expected_result = self._test_data_from('expected_result.txt')

        with TextDifferencesViewer(actual_result, expected_result_path):
            expect(actual_result).to(equal(expected_result))

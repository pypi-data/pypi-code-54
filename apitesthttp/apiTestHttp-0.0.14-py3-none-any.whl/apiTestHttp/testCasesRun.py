# coding:utf-8
# import allure
import getopt
import subprocess
import sys

import pytest

from apitestbasiclib.filetools import get_testcases
from apitestbasiclib.apitestlogic import apitest



def runCases():
    opts, args = getopt.getopt(sys.argv[1:], "-hf:e:", ["help", "file=", "env="])
    filepath = ''
    envname = ''
    for opt, value in opts:
        if opt == '-f' or opt == '--file':
            filepath = value
    test_cases = get_testcases(filepath)
    print('test_cases = %s' % test_cases)

    @pytest.mark.parametrize('test_cases', test_cases)
    def test_yamlapi(test_cases):
        apitest(test_cases, envname)
    # subprocess.Popen('pytest testCasesRun.py')
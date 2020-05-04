# coding:utf-8
# import allure
import getopt
import subprocess
import sys

import pytest

from apitestbasiclib.filetools import get_testcases
from apitestbasiclib.apitestlogic import apitest

try:
    opts, args = getopt.getopt(sys.argv[1:], "-hf:e:", ["help", "file=", "env="])
    print(opts)
except Exception:
    print('参数输入错误，请查看帮助文档')
    help()
    sys.exit(-1)
filepath = ''
envname = ''
for opt,value in opts:
    if opt == '-f' or opt == '--file':
        filepath = value
test_cases = get_testcases(filepath)
print(test_cases)

@pytest.mark.parametrize('test_cases',test_cases)
def test_yamlapi(test_cases):
    apitest(test_cases,envname)

def runCases():
    subprocess.Popen('pytest testCasesRun.py')
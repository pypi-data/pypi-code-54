
import helpdev


def test_run_subprocess_split():
    helpdev._run_subprocess_split("ls")

def test_check_float():
    output = helpdev.check_float()
    (isinstance(output, dict))

def test_check_thread():
    output = helpdev.check_thread()
    assert(isinstance(output, dict))

def test_check_python_packages():
    output = helpdev.check_python_packages()
    assert isinstance(output, dict)

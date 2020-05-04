from .run_process import run_process

def run():
    print("rm -rf - i dist/")
    return_code_rm_dist = run_process(["rm -rf - i dist/"])
    if (return_code_rm_dist != 0):
        print("[ERROR] There was an error in the deletion of dist/")
        return 1
    print("python3 setup.py sdist bdist_wheel ")
    return_code_build = run_process(["python3 setup.py sdist bdist_wheel "])
    if (return_code_build != 0):
        print("[ERROR] There was an error the building of the package")
        return 1
    print("python3 -m twine upload --repository pypi dist/*")
    return_code_publish = run_process("python3 -m twine upload --repository pypi dist/*")
    if (return_code_publish != 0):
        print("[ERROR] There was an error with the publishing of the package on pypi")
        return 1
    return 0


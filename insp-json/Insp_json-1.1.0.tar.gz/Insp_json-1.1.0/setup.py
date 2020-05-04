import pathlib
import setuptools
setuptools.setup(
    name="Insp_json",
    version="1.1.0",
    long_description=pathlib.Path("d:\\vcode\\HOLA!\\InspJson\\README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests","data"])
) 

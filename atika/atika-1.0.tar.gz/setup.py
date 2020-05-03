import setuptools
from pathlib import Path

# p =                      #
p = setuptools.find_packages(exclude=["tests", "data"])

setuptools.setup(
    name="atika",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=p,
)

# find_packages excude the given list of modules as they are not part of the source code
print("Publishing")

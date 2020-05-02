"""Completion, correction, and checking of numpydoc-style docstrings in Python."""

from setuptools import setup, find_packages

requires = [
    'astor>=0.8.1',
    'docstring-parser>=0.7.1'
]

extras = {
    'testing': [
        'coverage',
        'nose',
        'nose-timer',
        'rednose',
    ],
    'develop': [
        'autopep8',
        'bpython',
        'flake8',
        'jedi',
        'snakeviz',
        'yapf',
    ]
}

extras['complete'] = list({pkg for req in extras.values() for pkg in req})

setup(
    name='numpydoctor',
    use_scm_version=True,
    author='Rob Kelly',
    author_email='contact@robkel.ly',
    description=__doc__,
    url="https://gitlab.com/krampus/numpydoctor",
    entry_points={
        'console_scripts': ['numpydoctor = numpydoctor.__main__:main']
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.8',
    setup_requires=[
        'setuptools_scm'
    ],
    install_requires=requires,
    extras_require=extras
)

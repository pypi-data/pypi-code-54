from setuptools import find_packages, setup

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='ubot',
    version='6.0.0',
    author='Alessandro Cerruti',
    author_email='thereap3r97@gmail.com',
    description='Basic, easily extendable, Telegram bot class',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/strychnide/ubot',
    license='MIT',
    project_urls={
        'Source': 'https://github.com/strychnide/ubot',
        'Issues': 'https://github.com/strychnide/ubot/issues'
    },
    python_requires='>=3.6',
    extras_require={
        'mediainfo': ['libmediainfo_cffi'],
        'dev': [
            'flake8',
            'flake8-import-order',
            'flake8-quotes',
            'flake8-bugbear',
            # 'sphinx',
            # 'sphinx-autodoc-typehints',
            # 'sphinx_rtd_theme',
            'coverage',
            'twine'
        ]
    },
    packages=find_packages()
)

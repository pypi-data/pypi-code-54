#!/usr/bin/env3 python
"""QEMU tooling placeholder."""

import setuptools

def main():
    """
    QEMU tooling installation placeholder
    """

    kwargs = {
        'name': 'qemu',
        'version': '0.0.0a1',
        'maintainer': 'John Snow',
        'maintainer_email': 'qemu-devel@nongnu.org',
        'url': 'https://www.qemu.org/',
        'download_url': 'https://www.qemu.org/download/',
        'packages': setuptools.find_packages(),
        'description': 'QEMU Python Build, Debug and SDK tooling.',
        'classifiers': [
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
        ],
        'platforms': [],
        'keywords': [],
        'setup_requires': [
            'setuptools',
        ],
        'install_requires': [],
        'python_requires': '>=3.5',
        'long_description_content_type': 'text/x-rst',
    }

    with open("README.rst", "r") as fh:
        kwargs['long_description'] = fh.read()

    setuptools.setup(**kwargs)

if __name__ == '__main__':
    main()

import setuptools

setuptools.setup(
    name = 'section-explore',
    version = '1.1.2',
    url = 'https://github.com/theglossy1/section',
    author = 'theglossy1',
    author_email = 'develop@jemnetworks.com',
    license = 'License :: OSI Approved :: MIT License',
    description = 'Read a text/config file by sections',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    install_requires = [
       'more-argparse'
    ],
    py_modules = [
        'section',
        'section_run'
    ],
    entry_points = {
        'console_scripts': [
            'section=section_run:main'
        ]
    }
)
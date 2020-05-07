from setuptools import setup


with open('README.md') as file:
    long_description = file.read()


setup(
    name='modbusy',
    version='1.0.2',
    python_requires='>=3.6',

    packages=['modbusy'],

    include_package_data=True,
    package_data={
        'modbusy': ['py.typed'],
    },

    install_requires=[
        'gevent>=1.3',
        'uModbus>=1'
    ],

    extras_require={
        'cli': [
            'click>=6',
            'pyyaml',
            'voluptuous',
        ],
        'test': [
            'pytest>5.0,<6'
        ]
    },

    author='Brandon Carpenter',
    author_email='brandon@8minute.com',
    url='https://bitbucket.com/8minutenergy/modbusy',
    description='Easy library for writing Modbus slaves',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='BSD',
    zip_safe=True,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Embedded Systems',
        'Typing :: Typed',
    ]
)

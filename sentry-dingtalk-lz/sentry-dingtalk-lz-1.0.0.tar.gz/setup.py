from setuptools import setup, find_packages

from multiprocessing import util

tests_require = [
]

install_requires = [
    'sentry>=5.4.1',
]

setup(
    name='sentry-dingtalk-lz',
    version='1.0.0',
    author='leon zhang',
    author_email='leonzhang2008@gmail.com',
    url='https://github.com/leonzhang2008/sentry-dingtalk.git',
    description='A Sentry extension which integrates with Dinttalk robot.',
    long_description='A Sentry extension which integrates with Dinttalk robot.',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='nose.collector',
    entry_points={
        'sentry.plugins': [
            'dingtalk = sentry_dingtalk.plugin:DingtalkPlugin'
        ],
    },
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)

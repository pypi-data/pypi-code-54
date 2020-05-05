# coding=UTF-8

from setuptools import setup

setup(
    name='datazeus',
    version='0.0.1',
    author='Marcelo Horita',
    author_email='mfhorita@gmail.com.br',
    packages=['datazeus'],
    description='Busca de parâmetros para machine learning',
    long_description='Pacote de busca dos melhores parâmetros para machine learning',
    url='https://github.com/mfhorita',
    license='MIT',
    keywords='datazeus sklearn learn knn logistic naive bayes decision tree forests classifier',
    classifiers=[
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    install_requires=[
        'scikit-learn>=0.22.2',
        'pandas>=0.25.3'
    ]
)
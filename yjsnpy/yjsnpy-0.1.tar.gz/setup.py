from yjsnpy import __version__


try:
    from setuptools import setup, find_packages
    package = find_packages(exclude=['example', 'test', 'dist'])
except ImportError:
    from distutils.core import setup
    package = ['yjsnpy']


with open('requirements.txt', 'r') as f:
    req = f.read().split('\n')
if '' in req:
    req.remove('')


setup(
    name='yjsnpy',
    version=__version__,
    description='A Python implement for INM Universe',
    author='KumaTea',
    author_email='kumatea@protonmail.com',
    url='https://github.com/KumaTea/yjsnpy',
    license='MIT License',
    keywords=['yjsnpy', 'yjsnpi', 'inm'],
    packages=package,
    include_package_data=True,
    install_requires=req,
    setup_requires=req,
    classifiers=[
        'Development Status :: 3 - Alpha',      # 3 - Alpha, 4 - Beta or 5 - Production/Stable
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

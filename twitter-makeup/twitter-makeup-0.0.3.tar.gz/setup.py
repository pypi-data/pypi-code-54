from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='twitter-makeup',
    version='0.0.3',
    description='Make up your twitter profile, from 🐴 to 🦄 !',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=['twitter_makeup'],
    author='Nicolas Dupont',
    author_email='duponn@gmail.com',
    keywords=['Twitter', 'Profile', 'API'],
    url='https://github.com/nidup/twitter-makeup',
    download_url='https://pypi.org/project/twitter-makeup',
    include_package_data=True
)

install_requires = [
    'tweepy>=3.8.0'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)


import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = 'desktop-notify',
	version = '1.1.3',
	python_requires = '>=3.7',
	install_requires = [
		'dbus-python>=1.2.8',
	],
	entry_points = {
		'console_scripts': [
			'desktop-notify = desktop_notify:main',
		],
	},
	author = 'hxss',
	author_email = 'hxss@ya.ru',
	description = 'Util for sending desktop notifications over dbus.',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://gitlab.com/hxss/desktop-notify',
	packages = setuptools.find_packages(),
	classifiers = [
		'Programming Language :: Python :: 3.7',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX :: Linux',
		'Topic :: Utilities',
	],
)

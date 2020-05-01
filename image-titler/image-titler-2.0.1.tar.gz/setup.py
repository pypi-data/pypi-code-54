import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="image-titler",
    version="2.0.1",
    author="The Renegade Coder",
    author_email="jeremy.grifski@therenegadecoder.com",
    description="Adds a title and logo to an image using The Renegade Coder Featured Image style",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheRenegadeCoder/image-titler",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            'image-titler = image_titler.command:main',
            'image_titler = image_titler.command:main',  # For backwards compatibility
        ],
        "gui_scripts": [
            'image-titler-gui = image_titler.gui:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'titlecase',
        'pillow>=6.0.0',
        'pathvalidate',
        'piexif'
    ],
)

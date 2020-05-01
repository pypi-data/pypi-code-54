import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RazbiUtils",
    version="0.0.3",
    author="Razbi",
    author_email="radu.denis88@gmail.com",
    description="This is a wrapper around  win32api, pyautogui and pynput.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GloryToArstotzka/RazbiUtils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
    install_requires=['pyautogui',
                      'pywin32',
                      'opencv-python',
                      'pynput',
                      'win32gui',
                      ],
)








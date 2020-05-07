import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="django-multiplechoicefield",
        version="1.0.1",
        author="Olaf Ruehenbeck",
        author_email="olaf+pip@ruehenbeck.org",
        description="A Package for Django which adds a MultipleChoiceField for Models.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/oruehenbeck/django-multiplechoicefield",
        packages=setuptools.find_packages(),
        classifiers=[
            "Framework :: Django",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        django_requires='>=2.2.6'
        )

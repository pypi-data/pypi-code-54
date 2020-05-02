import setuptools
 
setuptools.setup(
     name='easy_selenium-pkg',    # This is the name of your PyPI-package.
     version='0.1',                          # Update the version number for new releases
              # The name of your scipt, and also the command you'll be using for calling it
     author="ankit.kothari",
    author_email="ankit.kothari@hotmail.com",
    description="This is a selenium easy library which has easy syntax build on selenium.all the things are running in background we are calling only functions..This is too easy for begineers",
    url="https://github.com/ankitk29kothari/Step2success/tree/master/Selenium-Web%20Automation/easy_selenium",
    packages=setuptools.find_packages(),
    
  	download_url = 'https://github.com/ankitk29kothari/Step2success/tree/master/Selenium-Web%20Automation/easy_selenium', 
    license = 'GPLv2',
    classifiers = [],
    python_requires='>=3.6',
)
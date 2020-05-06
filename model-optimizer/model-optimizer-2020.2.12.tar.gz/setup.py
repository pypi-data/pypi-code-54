from setuptools import setup, find_packages
setup(
    name="model-optimizer",
    version="2020.2.12",
    packages=find_packages(),
	package_data={'': ['*.txt']},
	include_package_data=True,
	entry_points ={ 
            'console_scripts': [ 
                'mo_onnx = mo.mo_onnx:main'
            ] 
        },
      install_requires=[
          'onnx>=1.1.2 ','networkx>=1.11','numpy>=1.12.0' ,'defusedxml>=0.5.0'
      ]
)

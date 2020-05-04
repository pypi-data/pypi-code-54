import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
setuptools.setup(
  name = 'calmatuc',
  version = '0.0.6',
  author = 'Nicolle Murcia, Karen Pulido, Miguel Ángel Camargo, Mateo Ruíz, Jorge Ali Pastran, Carlos Trujillo, Isaac Zainea',
  author_email = 'czaineam@ucentral.edu.co',  
  description = 'Calculadora de Funciones Universidad Central',
  url = 'https://github.com/MathMaxUC/calmatuc', # use the URL to the github repo
  install_requires=REQUIREMENTS,
  keywords = ['calculadora', 'matematicas', 'calculo', 'algebra lineal', 'estadistica'],
  packages=setuptools.find_packages(),
  classifiers=[
	"Programming Language :: Python :: 3",
	"License :: OSI Approved :: MIT License",
	"Operating System :: OS Independent",
  ],
)

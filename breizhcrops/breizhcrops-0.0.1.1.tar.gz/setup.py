from setuptools import setup, find_packages

#try:
    # for pip >= 10
#from pip._internal.req import parse_requirements
#except ImportError:
    # for pip <= 9.0.3
#    from pip.req import parse_requirements

#def load_requirements(fname):
#    reqs = parse_requirements(fname, session="test")
#    return [str(ir.req) for ir in reqs]

#with open('breizhcrops/requirements.txt') as fp:
#    install_requires = fp.read()

setup(name='breizhcrops',
      version='0.0.1.1',
      description='A Satellite Time Series Dataset for Crop Type Identification',
      url='http://github.com/dl4sits/breizhcrops',
      author='Marc Rußwurm, Charlotte Pelletier',
      author_email='marc.russwurm@tum.de',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            "geopandas>=0.5.0",
            "numpy>=1.17.0",
            "pandas>=0.24.2",
            "geojson>=2.4.1",
            "jupyter>=1.0.0",
            "matplotlib>=3.1.0",
            "seaborn>=0.9.0",
            "torch>=1.4.0",
            "tqdm>=4.32.2",
            "scikit-learn",
            "h5py",
            "requests"
      ],
      zip_safe=False)

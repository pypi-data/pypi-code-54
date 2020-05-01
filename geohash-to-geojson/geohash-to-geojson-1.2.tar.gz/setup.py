
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='geohash-to-geojson',  
     version='1.2',
     license="MIT",
     author="Afraoucene Chakib",
     author_email="fc_afraoucene@esi.dz",
     description="convert set of geohashes into a geojson boundaries files of the corresponding geohashes",
     long_description=long_description,
     url="https://github.com/brings123/geohash-to-geojson",
     packages=setuptools.find_packages(),
     long_description_content_type="text/markdown",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
         
     ],
     install_requires=[
       "polygon_geohasher",
       "geopandas",
       "shapely"
   ]
 )
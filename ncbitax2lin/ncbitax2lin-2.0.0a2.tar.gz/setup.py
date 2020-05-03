# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ncbitax2lin']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1,<0.4.0', 'pandas>=1.0.3,<2.0.0']

entry_points = \
{'console_scripts': ['ncbitax2lin = ncbitax2lin.ncbitax2lin:main']}

setup_kwargs = {
    'name': 'ncbitax2lin',
    'version': '2.0.0a2',
    'description': 'A tool that converts NCBI taxonomy dump into lineages',
    'long_description': '# NCBItax2lin\n\nConvert NCBI taxonomy dump from ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz\ninto lineages. An example for [human (tax_id=9606)](https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=9606) is like\n\n| tax_id | superkingdom | phylum   | class    | order    | family    | genus | species      | family1 | forma | genus1 | infraclass | infraorder  | kingdom | no rank            | no rank1     | no rank10            | no rank11 | no rank12 | no rank13 | no rank14 | no rank15     | no rank16 | no rank17 | no rank18 | no rank19 | no rank2  | no rank20 | no rank21 | no rank22 | no rank3  | no rank4      | no rank5   | no rank6      | no rank7   | no rank8     | no rank9      | parvorder  | species group | species subgroup | species1 | subclass | subfamily | subgenus | subkingdom | suborder    | subphylum | subspecies | subtribe | superclass | superfamily | superorder       | superorder1 | superphylum | tribe | varietas |\n|--------|--------------|----------|----------|----------|-----------|-------|--------------|---------|-------|--------|------------|-------------|---------|--------------------|--------------|----------------------|-----------|-----------|-----------|-----------|---------------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|---------------|------------|---------------|------------|--------------|---------------|------------|---------------|------------------|----------|----------|-----------|----------|------------|-------------|-----------|------------|----------|------------|-------------|------------------|-------------|-------------|-------|----------|\n| 9606   | Eukaryota    | Chordata | Mammalia | Primates | Hominidae | Homo  | Homo sapiens |         |       |        |            | Simiiformes | Metazoa | cellular organisms | Opisthokonta | Dipnotetrapodomorpha | Tetrapoda | Amniota   | Theria    | Eutheria  | Boreoeutheria |           |           |           |           | Eumetazoa |           |           |           | Bilateria | Deuterostomia | Vertebrata | Gnathostomata | Teleostomi | Euteleostomi | Sarcopterygii | Catarrhini |               |                  |          |          | Homininae |          |            | Haplorrhini | Craniata  |            |          |            | Hominoidea  | Euarchontoglires |             |             |       |          |\n\n## Regenerate the lineages yourself\n\nRegeneration is straightforward, but it may incur quite a bit of memory (~20\nGB). I generated `lineages.csv.gz` on a machine with 32 GB memory. Pull request\non refactoring to a lower memory usage is welcome. It\'s mainly about\n[this line](https://github.com/zyxue/ncbitax2lin/blob/master/ncbitax2lin.py#L184),\nwhere the `pool.map` takes places.\n\nIf you really need an updated version but without the hardware resources, you\ncould also notify me on github, and I will update it for you.\n\n### Install\n\n```\ngit clone git@github.com:zyxue/ncbitax2lin.git\ncd ncbitax2lin/\n```\n\n#### Set up a virtual environment\n\nCurrently, it only works with `python2.7`, and needs\n[pandas](http://pandas.pydata.org/), so make sure you are in a proper virtual\nenvironment. If you have already these had one available, just use that\none.\n\nOtherwise, you can create a new one with\n[miniconda](https://conda.io/miniconda.html)/[anaconda](https://www.continuum.io/downloads)\n(recommended),\n\n```\nconda create -y -p venv/ --file env-conda.txt\n# or effectively the same\n# conda create -y -p venv python=2 pandas\nsource activate venv/\n```\n\nor with [virtualenv + pip](http://docs.python-guide.org/en/latest/dev/virtualenvs/)\n\n```\nvirtualenv venv/\nsource venv/bin/activate\npip install -r env-pip.txt\n```\n\n### Regenerate\nThen run the following, this will download the latest taxdump from NCBI, and run\nthe scripts to regenerate all latest lineages from it\n\n```\nmake\n```\n\n## FAQ\n\n**Q**: I have a large number of sequences with their corresponding accession\nnumbers from NCBI, how to get their lineages?\n\n**A**: First, you need to map accession numbers (GI is deprecated) to tax IDs\nbased on `nucl_*accession2taxid.gz` files from\nftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/. Secondly, you can trace a\nsequence\'s whole lineage based on its tax ID. The tax-id-to-lineage mapping is\nwhat NCBItax2lin generates for you, and it is available on <a\nhref="https://gitlab.com/zyxue/ncbitax2lin-lineages/tree/master"\ntarget="_blank">ncbitax2lin-lineages</a>.\n\nIf you have any question about this project, please feel free to create a new\n[issue](https://github.com/zyxue/ncbitax2lin/issues/new).\n\n## Note on `taxdump.tar.gz.md5`\n\nIt appears that NCBI periodically regenerates `taxdump.tar.gz` and\n`taxdump.tar.gz.md5` even when its content is still the same. I am not sure how\ntheir regeneration works, but `taxdump.tar.gz.md5` will differ simply because\nof a different timestamp.\n\n## Used in\n\n* Mahmoudabadi, G., & Phillips, R. (2018). A comprehensive and quantitative exploration of thousands of viral genomes. ELife, 7. https://doi.org/10.7554/eLife.31955\n',
    'author': 'Zhuyi Xue',
    'author_email': 'zhuyi@alum.utoronto.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zyxue/ncbitax2lin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

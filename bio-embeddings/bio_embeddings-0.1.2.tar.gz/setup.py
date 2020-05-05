# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bio_embeddings',
 'bio_embeddings.embed',
 'bio_embeddings.embed.albert',
 'bio_embeddings.embed.fasttext',
 'bio_embeddings.embed.glove',
 'bio_embeddings.embed.seqvec',
 'bio_embeddings.embed.transformerxl',
 'bio_embeddings.embed.transformerxl.mem_transformer',
 'bio_embeddings.embed.transformerxl.mem_transformer.utils',
 'bio_embeddings.embed.transformerxl.utils',
 'bio_embeddings.embed.word2vec',
 'bio_embeddings.extract_features',
 'bio_embeddings.extract_features.features',
 'bio_embeddings.extract_features.seqvec',
 'bio_embeddings.project',
 'bio_embeddings.utilities',
 'bio_embeddings.utilities.filemanagers',
 'bio_embeddings.visualize']

package_data = \
{'': ['*']}

install_requires = \
['allennlp>=0.9.0,<0.10.0',
 'biopython>=1.76,<2.0',
 'gensim>=3.8.2,<4.0.0',
 'h5py>=2.10.0,<3.0.0',
 'lock>=2018.3.25,<2019.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.3,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'plotly>=4.6.0,<5.0.0',
 'ruamel_yaml>=0.16.10,<0.17.0',
 'scikit-learn>=0.22.2.post1,<0.23.0',
 'scipy>=1.4.1,<2.0.0',
 'torch>=1.5.0,<2.0.0',
 'tqdm>=4.45.0,<5.0.0',
 'transformers>=2.8.0,<3.0.0',
 'umap-learn>=0.4.2,<0.5.0']

entry_points = \
{'console_scripts': ['bio_embeddings = bio_embeddings.utilities.cli:main']}

setup_kwargs = {
    'name': 'bio-embeddings',
    'version': '0.1.2',
    'description': 'A pipeline for protein embedding generation and visualization',
    'long_description': '# Bio Embeddings\nThe project includes:\n\n- A pipeline that allows to embed a FASTA file choosing from various embedders (see below), and then project and visualize the embeddings on 3D plots.\n- A web server that takes in sequences, embeds them and returns the embeddings OR visualizes the embedding spaces on interactive plots online.\n- General purpose library to embed protein sequences in any python app.\n\n## Important information\n\n- The `albert` model weights are not publicly available yet. You can request early access by opening an issue.\n- Please help us out by opening issues and submitting PRs as you see fit, this repository is actively being developed.\n\n## Install guides\n\nYou can install the package via PIP like so:\n\n```bash\npip install bio-embeddings\n```\n\nOr directly from the source (e.g. to have the latest features):\n\n```bash\npip install -U git+https://github.com/sacdallago/bio_embeddings.git\n```\n\n### Additional dependencies and steps to run the webserver\n\nIf you want to run the webserver locally, you need to have some python backend deployment experience.\nYou\'ll need a couple of dependencies if you want to run the webserver locally: `pip install dash celery pymongo flask-restx pyyaml`.\n\nAdditionally, you will need to have two instances of the app run (the backend and at least one celery worker), and both instances must be granted access to a MongoDB and a RabbitMQ or Redis store for celery.\n\n## Examples\n\nWe highly recommend you to check out the `examples` folder for pipeline examples, and the `notebooks` folder for post-processing pipeline runs and general purpose use of the embedders.\n\nAfter having installed the package, you can:\n\n1. Use the pipeline like:\n\n    ```bash\n    bio_embeddings config.yml\n    ```\n\n    A blueprint of the configuration file, and an example setup can be found in the `examples` directory of this repository.\n\n1. Use the general purpose embedder objects via python, e.g.:\n\n    ```python\n    from bio_embeddings import SeqVecEmbedder\n\n    embedder = SeqVecEmbedder()\n\n    embedding = embedder.embed("SEQVENCE")\n    ```\n\n    More examples can be found in the `notebooks` folder of this repository.\n \n## Development status\n\n1. Pipeline stages\n    - embed:   \n        - [x] SeqVec v1/v2 (https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3220-8)\n        - [ ] TransformerXL\n        - [ ] Fastext\n        - [ ] Glove\n        - [ ] Word2Vec\n        - [ ] UniRep (https://www.nature.com/articles/s41592-019-0598-1?sfns=mo)\n        - [x] Albert (unpublished)\n    - project:\n        - [x] t-SNE\n        - [x] UMAP\n    \n1. Web server:  \n    - [x] SecVec\n    - [x] Albert (unpublished)\n    \n1. General purpose objects:\n    - [x] SecVec\n    - [x] TransformerXL\n    - [x] Fastext\n    - [x] Glove\n    - [x] Word2Vec\n    - [ ] UniRep\n    - [x] Albert (unpublished)\n    \n\n## Building a Distribution\nBuilding the packages best happens using invoke.\nIf you manganage your dependecies with poetry this should be already installed.\nSimply use `poetry run invoke clean build` to update your requirements according to your current status\nand to generate the dist files\n\n## Contributors\n\n- Christian Dallago (lead)\n- Tobias Olenyi\n- Michael Heinzinger\n',
    'author': 'Christian Dallago',
    'author_email': 'christian.dallago@tum.de',
    'maintainer': 'Rostlab',
    'maintainer_email': 'admin@rostlab.org',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

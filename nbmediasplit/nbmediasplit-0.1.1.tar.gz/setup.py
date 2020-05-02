# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['nbmediasplit']
install_requires = \
['beautifulsoup4>=4.9,<5.0', 'click>=7.1,<8.0', 'lxml>=4.5,<5.0']

entry_points = \
{'console_scripts': ['nbmediasplit = nbmediasplit:main']}

setup_kwargs = {
    'name': 'nbmediasplit',
    'version': '0.1.1',
    'description': '',
    'long_description': '# nbmediasplit\n\n`nbmediasplit` is a script to extract base64 encoded image and audio pcm embedded in .ipynb file and save them into specified directories.\n\n## install\n\n`pip install nbmediasplit`\n\n## usage\n\n### extract image files from ipynb\n\n`nbmediasplit -n input.ipynb -i image_out_dir`\n\nor\n\n`nbmediasplit --ipynb input.ipynb --imgdir image_out_dir`\n\nAbove command extract image files from `input.ipynb` and store them to `image_out_dir`.\n`-n` or `--ipynb` specifies input ipynb file.\n`-i` or `--imgdir` specifies directory to store image files.\nFilenames of stored image are numbered in a sequential order(`0.png`, ...).\n\n### extract audio files from ipynb\n\n`nbmediasplit -n input.ipynb -w wav_out_dir`\n\nor\n\n`nbmediasplit --ipynb input.ipynb --wavdir wav_out_dir`\n\nAbove command extract audio files from `input.ipynb` and store them to `wav_out_dir`.\n`-n` or `--ipynb` specifies input ipynb file.\n`-w` or `--wavdir` specifies directory to store audio files.\nFilenames of stored audio are numbered in a sequential order(`0.wav`, ...).\n\n### extract image and audio files from ipynb\n\n`nbmediasplit -n input.ipynb -i image_out_dir -w wav_out_dir`\n\nor\n\n`nbmediasplit --ipynb input.ipynb --imgdir image_out_dir --wavdir wav_out_dir`\n\nAbove command do below things.\n\n* extract image files from `input.ipynb` and store them to `image_out_dir`\n* extract audio files from `input.ipynb` and store them to `wav_out_dir`.\n\n`-n` or `--ipynb` specifies input ipynb file.\n`-i` or `--imgdir` specifies directory to store image files.\n`-w` or `--wavdir` specifies directory to store audio files.\nFilenames of stored image are numbered in a sequential order(`0.png`, ...).\nFilenames of stored audio are numbered in a sequential order(`0.wav`, ...).\n\n### extract image and audio files from ipynb and convert ipynb\n\nIf you use `-o` or `--output` option like below command,\nyou can convert `input.ipynb` to new ipynb file which refers stored image files and audio files directly.\n\n`nbmediasplit -n input.ipynb -i image_out_dir -w wav_out_dir -o converted.ipynb`\n\nor\n\n`nbmediasplit --ipynb input.ipynb --imgdir image_out_dir --wavdir wav_out_dir --output converted.ipynb`\n\nAbove command extract image files and audio files, and store them to specified directories, and generate new ipynb file `converted.ipynb`.\n`converted.ipynb` includes same content as `input.ipynb`, but base64 encoded image and audio data are replaced to html tag refers stored files directly like below.\n\n* image tag\n    * `<img src="${image_out_dir}/${n}.png" />`\n* audio tag\n    * `<audio controls preload="none"><source  src="${wav_out_dir}/${n}.wav" type="audio/wav" /></audio>`\n\nAlso, you can use `--img-prefix` and `--wav-prefix` options.\nThese options can change the path embeded in src attribute of output html like below(actual files are stored `image_out_dir` and `wav_out_dir`).\n\n* image tag\n    * `<img src="${img-prefix}/${n}.png" />`\n* audio tag\n    * `<audio controls preload="none"><source  src="${wav-prefix}/${n}.wav" type="audio/wav" /></audio>`\n\n### show help\n\n`nbmediasplit --help`\n\n## note ##\n\nUnless you trust the notebook converted by nbmediasplit in jupyter, you can\'t load audio source because of html sanitaization.\nTo trust notebook in jupyterlab, go to command pallet in left sidebar(on osx, type `shift+cmd+c`) and execute `trust notebook`,\nthen you\'ll load audio source if the source path is correct.\n',
    'author': 'wrist',
    'author_email': 'stoicheia1986@gmail.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)

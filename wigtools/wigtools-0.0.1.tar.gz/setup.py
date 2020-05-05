# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wigtools']

package_data = \
{'': ['*']}

install_requires = \
['attrs', 'diot', 'pyparam']

entry_points = \
{'console_scripts': ['wigtools = wigtools:main']}

setup_kwargs = {
    'name': 'wigtools',
    'version': '0.0.1',
    'description': 'A set of tools for wiggle file',
    'long_description': '# wigtools\nA set of tools for wiggle file\n\n## Installation\n```\npip install wigtools\n```\n\n## Usage\n```bash console\n> wigtools\n\nDescription:\n  A set of tools for wiggle file\n\nUsage:\n  wigtools <command> [OPTIONS]\n\nGlobal optional options:\n  -h, -H, --help      - Show help message and exit.\n\nAvailable commands:\n  switch-base         - Switch the coordinate base of a wiggle file.\n  sort                - Sort the blocks in a wiggle file by chrom and start. Chromosomes will be \\\n                        sorted the way  sort -V  does.\n  stats               - Statistics for data in a wiggle file for each block\n  reshape             - Generate a new wiggle file and reshape the blocks to the query regions\n  query               - Find the blocks that intersect with the query regions\n  help [COMMAND]      - Print help message for the command and exit.\n```\n\n### Switch coordinate base for a wiggle file\n\n```bash console\n> cat test.wig\nvariableStep chrom=chr\n1\t1.0\n2\t2.0\n\n> cat test.wig | wigtools switch-base --to 0\nvariableStep chrom=chr span=1\n0\t1.0\n1\t2.0\n```\n\n### Sort a wiggle file\n\n```bash console\n> cat test-unsorted.wig\nvariableStep chrom=chr\n5\t1.0\n6\t2.0\nvariableStep chrom=chr\n1\t1.0\n2\t2.0\n\n> cat test.wig-unsorted.wig | wigtools sort\nvariableStep chrom=chr span=1\n1\t1.0\n2\t2.0\nvariableStep chrom=chr span=1\n5\t1.0\n6\t2.0\n```\n\n### Calculate the statistics of each block\n\n```bash console\n> cat test-unsorted.wig | wigtools sort | wigtools stats\nChrom   Start   End     min     max     mean    median  sum     count   bp\nchr     1\t2\t1.0     2.0     1.5     1.5     3.0     2\t2\nchr     5\t6\t1.0     2.0     1.5     1.5     3.0     2\t2\n\n> cat test-unsorted.wig | wigtools sort | wigtools stats --stats mean count --nohead\nchr     1\t2\t1.5     2\nchr     5\t6\t1.5     2\n```\n\n### Query a wiggle file to find blocks\n\n```bash console\n> cat query.bed\nchr\t2\t3\n\n> wigtools query -i test-unsorted.wig --qfile query.bed\nvariableStep chrom=chr span=1\n1\t1.0\n2\t2.0\n\n> wigtools query -i test-unsorted.wig --qfile query.bed --qbase 0\n# No overlapping blocks\n```\n\n### Reshape the blocks in query regions\n\n```bash console\n> cat reshape.bed\nchr\t1\t8\n\n> cat test-unsorted.wig | wigtools sort | wigtools reshape --qfile reshape.bed\nvariableStep chrom=chr span=1\n1\t1.0\n2\t2.0\n5\t1.0\n6\t2.0\n```',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/wigtools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

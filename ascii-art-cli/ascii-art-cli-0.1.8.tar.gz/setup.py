# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ascii_art_cli']
install_requires = \
['pillow>=6.2.1,<7.0.0']

entry_points = \
{'console_scripts': ['ascii-art = ascii_art_cli:main']}

setup_kwargs = {
    'name': 'ascii-art-cli',
    'version': '0.1.8',
    'description': 'ASCII art generator with multiple customization parameters',
    'long_description': '<div align="center">\n<img src="https://raw.githubusercontent.com/dawsonbooth/ascii-art/master/logo.png" alt="ascii-art">\n\n[![](https://img.shields.io/pypi/v/ascii-art-cli.svg?style=flat)](https://pypi.org/pypi/ascii-art-cli/)\n[![](https://img.shields.io/pypi/dw/ascii-art-cli.svg?style=flat)](https://pypi.org/pypi/ascii-art-cli/)\n[![](https://img.shields.io/pypi/pyversions/ascii-art-cli.svg?style=flat)](https://pypi.org/pypi/ascii-art-cli/)\n[![](https://img.shields.io/pypi/format/ascii-art-cli.svg?style=flat)](https://pypi.org/pypi/ascii-art-cli/)\n[![](https://img.shields.io/pypi/l/ascii-art-cli.svg?style=flat)](https://github.com/dawsonbooth/ascii-art/blob/master/LICENSE)\n\n</div>\n\n# Description\n\nNamed as such, this package is a command-line ASCII art generator written in Python. There is a variety of customization parameters which are detailed below.\n\n# Installation\n\nWith Python installed, install the package from PyPI with the following command:\n\n```bash\npip install ascii-art-cli\n```\n\nThis package is not to be confused with [ascii_art](https://pypi.org/project/ascii_art/) or other various ASCII art packages.\n\n# Usage\n\nThis is a command-line program, and can be executed as follows:\n\n```bash\nascii-art [-h] [--output OUTPUT] [--width WIDTH] [--height HEIGHT] [--chars CHARS] [--font FONT] [--invert] [--normalize] [--terminal] input\n```\n\nPositional arguments:\n\n```\ninput: Path to image from which ASCII art will be generated\n```\n\nOptional arguments:\n\n```\n  -h, --help        Show the help message and exit\n  --output OUTPUT   Path to output generated ASCII art\n  --width WIDTH     Character width of ASCII art\n  --height HEIGHT   Character height of ASCII art\n  --chars CHARS     Path to characters to be seen in ASCII art\n  --font FONT       Font for calculating the character weights\n  --invert          Whether the ASCII output color is inverted\n  --normalize       Whether the weights of the provided ASCII characters are normalized\n  --terminal        Whether to output to the terminal\n```\n\nExample:\n\n```bash\nascii-art examples/images/einstein.jpg --width 100 --height 50 --font "Courier" --terminal --normalize\n```\n\n```\n%%++%+++%%;+;%%+%%%%%S%%+SSSSSS+,\'%++;\'\',\'\'\'.\'\'\'\'.\'\'\'.\'.\'\'\'\'.\'\'\'\'\',,,,,,;;,,,\'%S\'+##@@@@#@@@@@@@@@@#\n+++%;%+%%++%+SS%S%+%S%%SS%S%S%+,\'S%;\',\'....\'\'... .............\'.\'\',\',,,;,;,\',\'\'+S,S#@@@@@@@@@@@@@@@@\n;++%S%++%%++%++%%%%%%SSSSSS%%;,,SS\',\',..........................\'\'.\'\'\';\'\',,,,\',,;%%##@@@@@@@@@@@@##@\n;++;++;++%%%%+S%%%SSSSSSSS%+%,;%S;+,..\'\'............ ...   ...\'\'..\'\'.,\',\',;,,,\'\',S,SS@@@@@@@@####@#@\n;;;;;%+;;+%%+S%+SSSSSSSS++%++%+SS,,;\'\'.. . .... ....     ...\'..\'\'\'.\'\'\',\'\',,,,\'\'\',;#S%S@@@#@@@@###@@@\n;++;;++%%+++%%%%SSSSSSS+;;,;S%SS,%,\'\'....... ... ..   ..  . ..\'\'.\'\'\'.\'\',,\',,,\'\'\'\',%;###S#@@@@@@@@@@#\n+;,+%++%++%S%SSSSSSS%%.;%SS%+SS+%\',;,\'... .. ....... ..  ...\'...\'\'\'\'\'\',\'\',,,\'\',\',\';,#@@#S@@@@#@@@@@@\n;;;%%+++%%+%%%SSSSS%,\'S;%%+SS;#+;,\'\',....  . ... ... ............\'\'\'\'.\'\'\'\',,\'..\'\',+S%##@#S@@@@#@@@@@\n;;+;+%;++%%%%SSSS%S%;S%S%++S+,#+,S##S+%\'............\',SS%\'\',..,..\'\'\'\'\'.\'\'\'\'\'\'\'.\',,\'%+%#@@#S@@@@@@@@@\n,+++;+%++%++%%SSSSS;S#;+;+%%;;#SS##SS,\'\'. ........\'.\'\'.;%%%,;;.\'\'.\'\'\'\'\'\'\'\'\'\'\'.\'\'\';;,%S+S####@@@@@@@@\n.;;;;++++%++++SSS%%,S%+S,;SS,%#,%+,\',,\'\'\'.. .... ... ..\'.\'..\'.....\',\'\'.\'\'\',\'\'.\'\'\';;++SSS###S@@@@@@@@\n;%;+%+;%++%%%S%%S+%SS#,;+SS;,+#+;\'\'\'\'\'\'......  .  ..............\',\'\'\'..\'\'\'\'\'.\'.\';,;;;;SSS#@####@@@@#\nS.+%%%;;%%%+%SSSSS#S#SS,+SS+;%#,\'\'.,,,\',,\'...     .\'.............\'\'\'\'\'\'\'\'\'\',\'.\',,,;S+;%+#S@@@#@@@@@@\n,,;%++;%%%+SSSSS#S###S+%%S%%;SS,.\';;;;;\'\';,.    .....\',;+S%,\'....\',\'..\'\'\'\'\'....\'\'\',,%%+;%SS#@@@#@@@@\n\';,++%+%%%S%SS%##S#SSS;SSSS+,#S;\';%S;+;.\'\'%;..  ....\'.\';+,,,+,...\',\'\'\'\'.\'\'\'.\'...\'\',,;+;%,,S@#@@@@@@@\n.%+%++%+%SSSSS#######S,SSSS%;#S;;S#. %%;+\';S.  ...\',\';+S%#%\',,\'\'\'\',\'..\'\';.\'\'\'..\'\'\',\';+;+;%%\'#@@@@@@#\n,,;++%%%%SSS########SS,SSSS,%#%,\'S+.###%.,,S.....,\'\',;..###S;\',...,\'\'\',\',\'\'\'\'..\'\'\'+,,;+%,,%S#%@@@@@@\nS+;+%S%%%SSS#####@##SS;SSSS,#S%,\'%+,%S,,%,S,\'...\', \',\'\'\'###.;\'\'\'\'.\'\'\'.\'\'\'\'\'\'\'\'\',\',,,;;;;+++%##S#@@@@\n%,S+%%%SSSSS######S+#S%#SS#+#S%,S%SS;;\'%.\'S,...\'\'\'.\',,;;,,\';+,\'\'\'.\'\'\'\'\',,,\'\'\'\',;;,;;,+;,;+S++@@%@@@@\n\',SSS%+S#SSS####S##S@+,##S#+#S+%;,;%;,\',;SS;.\'\'\'\'.\'\';,\'\',,,,,,\',,..\'\'.\'\'\'\'\'.\'\',;,,,,;,;S,+%S+%@@@@@@\n\',SSSS#%SSS####S#####%S##S###%;%;,,,,,,,;S+.\'.,\'.\'...\',,\'\'\'.\'\',,\'..\',\'\',,,,\',,,,++%;,\',,+\';S+SS@S@@@\n,%##SS#S#S#####S####%#SS#S###;;\',\'.\'\',..SS,\'.,,\'\'\'......\'.\'\'\'\'\'\',\'\'\',,\',,,,,;,;;\',SS+\',,,;,+S+##@#@@\n;S#@###SS##########+#SS##\'###%,\'\'\'\'..\'.,S;\'\'\'\',;,.\'.. .....\'.\'...\'.\',,,,,,,\',,%;\'\'%,%%;;,;,;;;%#@#@@\n+S@@####SS######S#;SSS###%###;\'...;...,%+.\'\'\',,,,\'..\'... ..........,,,,;,+++\';;\'.,+;%#,,\'\'\',,;+####@\n;#@@#@@#########S#S######S###;\'..\',\'\',\'S\'.....\',;,\'. ...... .. ...\'\';,;,,+%,+\'\'..\'\'#,,;,\'\'\',%,,S%#@@\nS#@###@############@####SS###+.\'\'\'\'\'\'.S%\'.   ..,\',,\'.  .. ........\',,+;,;+%,,..\'.,,.,.#,..\'\',;\'+S#@@\n####@##@#@############S###S##+,\'\'\'\'..\'%S,.  ..\'\'\'.,,\'.    . ......\'\';%,,,%%,\'....\'..\'.;%...\',;\',S@#@\n;%@####@@####@####S#######S##%;,;\'. .S%SS\'..\'\',\'..\';\'.\'    .......\'\',%,,;;++;,,.\';,..\',+...\'%;\',%#S#\nS%####@#@##@@##@#########%S##+++,\'..\'\';S#+,,,%.. ,,,...\'..  ..\'..+\'\',;,,;;%,..,\',\',\'.\',+..\'.++\';;#@@\n,+##@####@@@##@###@##,S+\'SS##+,%\'..\',,;\'\'\'\' .\'.\'\'\'......\'........\'\'\'+;,+,,+...,\'%\'\'.,\'+...\'.;+\'%SS#@\n%S@@, ###@#\'#@@#####@##@#####,\'%,\'\'\'\'\'\'.....\'.. \'..\',..\'\'\'...\'.\'...\',,,,;,S\'..;+;;;\',,,..\'\'.S%,%@###\nS%@@@#########@@###@#@@#SSS##,\'+\',.,..  .\'..,...\'...\'.\'\'\'\'....\'\'..\'\'+,,;,;+\'\'\';S;,;;;+\'\',\',,%,%@S@##\n%S@#@@@#@#@@#######@#####S###%\'%,%;.\',\' \'.... .\'\'...,.\'\'\'\'+..\'....\',+,,,,+,.\'\';;##\'\',,\'%%\'.;%#######\n#@@@###.#@@##@#@@##@#########S;%,;+%,,,\'\' .\'\'.,..,,,\',\'.\'.\'..\'....\',%\',,,%#\',;#@##%\'+%;#S,S#@#######\nS@@#@#@######@@####@#########S,+\',;%#S%;%,%,++\',SS,S;\',.\'.\'.\'.....\',;,\',;;S@@@@@@@@#S#@@#%S#########\n#@@##@@#@###@@@###############,;;\'\'%S#S#%#;S%%%+\'\'%S+S+#..\'\'..\'.\'.\',%\'\',+%S@@@@@@@@@@@@#@###########\n@@@##@@@##@@#######@##########;\'S\'..,SSS;%;,;,,,\',%;%##%%\'.\'..\'...\';%.\';+S@@@@@@@@#@@@#@###########S\n@@@@@@@@#@#####@###############+,+..\';#,.;,\';\',\',,,;S#++\',;..\'....\';\'\'\'%@@@@@@@@@@@#@###@#####S##S%%\n@@@@@#@@@@#@#@@################;\'%\'..,#\',,,,,;\';\',;SS,\'..\';.\',\'...\'%\',%@@@@@@@@@##@#####@#######SS%S\n@@@@@@@@@#######################,\';. \'#\' ,\';\',,+\'.%,;,,...,\'\',....+\'\'#@@@@@@@@@@@@@@###@######@S#+%S\n@@@@@@@#@#@###@#################S\'+...#+\'\',,%,,+.%S+;,\'..\',\'\',...\',.@@#@@@@@@@#@@@###@@#######SS+SS+\n@@@@@@@@@@@@#####################+\'\' \'#+\'.\'.\'%%,\'%S%;.....\'.;...,S\'#@@@@@@@#@@@#@####@#####@#SS+S%SS\n@@@@@@@@@@SSSSSS##################\'S.\'##, \'\',;+\',S+,\',....\'.%..\'+#@#@@#@@#@@#@@@#@@##@#@####%%+SS%SS\n@@@@@@#@SSS%SSSS#############S####S\'\'\'%#,\'.+,,,\'%,\',\'......\'...;###@@@@@@##@#@@####@#####@SS%SSS+SSS\n@@@@@@SS%SSSS%SSSS#################,S\'\'#%\'.,,;\';+,\'.... ...;.\'S##@@@##@@@#@#@@#@#@@@#@@@#SS%++S+S%+S\n@@@@%%SSS%S%S%SSS###################S;\',#;,;\',;S...\'\'.. ..\'\'\'####@@###@@@##@#####@##@###S++;;S%SSSS#\n#@%SS%%%S%%SS%S%SSS#######S#SS########;\'##,,,,;\'.....\'...\',########@@@@@#@@#######@@@##%%S%S%%S%#S##\nSS%S%%%S%%SSS%S%%SSS#####S#S#S#########;\'##++%.. ..\'....\'%####################@###@@@#SSSSSS%%%+SS##\n%SS%S%%%%SSS%S%%SSSS######SS##SSS#######,,+S,. ... ....,############@###########@@@#SS%+%%#+%%S+S###\nS%%%S+%%%%%%%%%S%%S###SS##SSSS###########;,\'\'........,############@#############@@##S%SSSSS,%SSSS##S\n```\n\n# License\n\nThis software is released under the terms of [MIT license](LICENSE).\n',
    'author': 'Dawson Booth',
    'author_email': 'pypi@dawsonbooth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dawsonbooth/ascii-art',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)

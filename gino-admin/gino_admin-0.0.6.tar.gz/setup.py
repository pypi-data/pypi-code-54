# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gino_admin', 'gino_admin.routes']

package_data = \
{'': ['*'], 'gino_admin': ['static/*', 'templates/*']}

install_requires = \
['Sanic-Jinja2>=0.7.5,<0.8.0',
 'Sanic>=19.12.2,<20.0.0',
 'aiofiles>=0.5.0,<0.6.0',
 'expiring_dict>=1.1.0,<2.0.0',
 'gino>=0.8.7,<0.9.0',
 'passlib>=1.7.2,<2.0.0',
 'sanic-auth>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'gino-admin',
    'version': '0.0.6',
    'description': 'Admin Panel for DB with Gino ORM and Sanic (inspired by Flask-Admin)',
    'long_description': 'gino_admin\n----------\nAdmin Panel for PostgreSQL DB with Gino ORM and Sanic\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/table_view_new.png\n  :width: 250\n  :alt: Table view\n\n\nHow to install\n--------------\n\n.. code-block:: python\n    \n    pip install gino_admin\n    \n\nUsage example\n-------------\n\nFull example placed in \'examples\' folder:\n\n.. code-block:: python\n    \n    examples/\n\n\nHow to use\n----------\n\n\nCreate in your project \'admin.py\' file and use `add_admin_panel` from from gino_admin import add_admin_panel\n\n\nExample:\n\n.. code-block:: python\n    \n    \n    from from gino_admin import add_admin_panel\n    \n    \n    add_admin_panel(\n        app, db, [User, Place, City, GiftCard], custom_hash_method=custom_hash_method\n    )\n        \n    \nWhere:\n\n    \'app\' - your Sanic application\n    \'db\' : from gino.ext.sanic import Gino; db = Gino() and [User, Place, City, GiftCard] - list of models that you want to add in Admin Panel to maintain\n        \n    custom_hash_method - optional parameter to define you own hash method to encrypt all \'_hash\' columns of your Models.\n    In admin panel _hash fields will be displayed without \'_hash\' prefix and fields values will be  hidden like \'******\'\n\n\nOr you can use admin as a standalone App, when you need to define Sanic Application first (check \'example\' folder)\n\n\nVersion 0.0.6 Updates:\n----------------------\n1. Clean up template, hide row controls under menu.\n2. Added \'Copy\' option to DB row.\n3. Now errors showed correct in table view pages in process of Delete, Copy, CSV Upload\n4. Added possible to work without auth (for Debug purposes). Set env variable \'ADMIN_AUTH_DISABLE=True\'\n5. Template updated\n6. Added export Table\'s Data to CSV\n7. First version of SQL-query execution (run any query and get answer from PostgreSQL)\n8. Fixed error display on csv upload\n\n\nVersion 0.0.5 Updates\n----------------------\n\n1. Upload from CSV: fixed upload from _hash fields - now in step of upload called hash function (same as in edit, or add per item)\n2. Fixed errors relative to datetime fields edit, added datetime_str_formats field to Config object, that allows to add custom datetime str formats. They used in step of convert str from DB to datetime object.\n3. Now \'_hash\' fields values in table showed as \'***********\'\n4. Fixed errors relative to int id\'s. Now they works correct in edit and delete.\n5. Update Menu template. Now if there is more when 4 models - they will be available under Dropdown menu.\n\n\nVersion 0.0.4 Updates:\n----------------------\n\n1. Upload from CSV - works, added example to `examples/` files. You can upload data from \'.csv\' tables.\n2. Edit per row - now exist button \'edit\'.\n3. Fixed delete for ALL rows of the model\n4. Fixed delete per element.\n5. Now works full \'CRUD\'.\n6. Fixed auth, now it sets \'cookie\' and compare user-agent (for multiple users per login)\n\nAuthentication\n--------------\n\n1. To disable authorisation:\n\nSet environment variable \'ADMIN_AUTH_DISABLE=1\'\n\n.. code-block:: python\n\n    os.environ[\'ADMIN_AUTH_DISABLE\'] = \'1\'\n\nor from shell:\n\n.. code-block:: python\n\n        export ADMIN_AUTH_DISABLE=1\n\n\n2. To define admin user & password:\n\ncheck example/ folder to get code snippets\n\n\n.. code-block:: python\n\n    app = Sanic()\n\n    app.config["ADMIN_USER"] = "admin"\n    app.config["ADMIN_PASSWORD"] = "1234"\n\n\nLimitations\n-----------\n\nFor correct work of Admin Panel all models MUST contain unique \'id\' field.\n\'id\' used to identify row (one element) for Edit & Delete operations.\n\nso if you define model, for example, User:\n\n.. code-block:: python\n\n    class User(db.Model):\n\n        __tablename__ = "users"\n\n        id = db.Column(db.String(), unique=True, primary_key=True)\n\nid also can be Integer/BigInteger:\n\n\n.. code-block:: python\n\n    class User(db.Model):\n\n        __tablename__ = "users"\n\n        id = db.Column(db.BigInteger(), unique=True, primary_key=True)\n\nSupported operations\n--------------------\n\n- One user auth\n- Create item by one for the Model\n- Delete all rows\n- Delete one item\n- Copy existed element (data table row)\n- Edit existed data\n- Upload data from csv\n\n\nTODO:\n\n- Select multiple for delete/copy\n- Deepcopy element (recursive copy all rows/objects that depend on chosen as ForeignKey)\n- Edit multiple\n- Multiple users\n- Set up data presets (drop table for some data state, defined from csv)\n- Filters in columns\n- Actions history\n\n\n\nContributions\n---------------\n\nContributions and feature requests are very welcome!\n\n\nIf you have time and want to fix:\nPlease open issues with that you want to add\nor write to me in Telegram: @xnuinside or mail: xnuinside@gmail.com\n\n\nDeveloper guide\n_______________\n\nProject use pre-commit hooks, so you need setup them\n\nJust run:\n\n.. code-block:: python\n\n    pre-commit install\n\nto install git hooks in your .git/ directory.\n\n\nScreens:\n--------\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/table_view_new.png\n  :width: 250\n  :alt: Table view\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/copy_item.png\n  :width: 250\n  :alt: Features per row\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/sql_runner.png\n  :width: 250\n  :alt: SQL-runner\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/add_item.png\n  :width: 250\n  :alt: Add item\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/auth.png\n  :width: 250\n  :alt: Simple auth\n\n.. image:: https://github.com/xnuinside/gino_admin/blob/master/docs/img/display_errors_on_upload_from_csv.png\n  :width: 250\n  :alt: Display errors on upload data from CSV\n\n\n',
    'author': 'xnuinside',
    'author_email': 'xnuinside@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xnuinside/gino_admin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

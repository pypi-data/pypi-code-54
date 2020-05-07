from setuptools import setup, find_packages

setup(
    name="noia-inspector",
    version='0.3.39',
    py_modules=['sdn_cli', 'settings'],
    install_requires=[
        'requests==2.22.0',
        'flask==1.1.1',
        'python-dotenv==0.10.3',
        'flask-restplus==0.13.0',
        'scapy==2.4.3',
        'ipwhois==1.1.0',
        'jinja2==2.11.1',
        'speedtest-cli==2.1.2',
        'pythonping==1.0.8',
        'icmplibv2==1.0.5',
        'Werkzeug==0.16.1',
        'pyroute2==0.5.12',
        'Click',
    ],
    packages=find_packages(),
    data_files=[('noia-inspector', ['settings/default.env', 'settings/destinations.json'])],
    entry_points='''
        [console_scripts]
        noia-inspector=sdn_cli:connect_sdn
        noia-api=sdn_cli:run_api
        noia-inspector-test=sdn_cli:run_tests
        noia-inspector-pinger=sdn_cli:run_pinger
    ''',
)

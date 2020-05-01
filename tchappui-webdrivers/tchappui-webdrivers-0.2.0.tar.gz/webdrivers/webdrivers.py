"""Main module."""

from io import BytesIO
from subprocess import run

from requests import get


def install_latest_chromedriver():
    """Downloads and installs the latest chromedriver for linux64."""
    version = get(
        "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    ).text
    url = (
        "https://chromedriver.storage.googleapis.com"
        f"/{version}/chromedriver_linux64.zip"
    )
    with open('/tmp/chromedriver.zip', 'wb') as f:
        f.write(get(url).content)
    return run([
        'sudo', 'unzip', '/tmp/chromedriver.zip', '-d', '/usr/local/bin'
    ])


def install_latest_geckdriver():
    """Downloads and installs the latest geckodriver for linux64."""
    response = get(
        "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
    )
    urls = [
        asset['browser_download_url']
        for asset in response.json().get('assets', [])
        if "linux64" in asset.get('name', '')
    ]
    for url in urls:
        with open('/tmp/geckodriver.tar.gz', 'wb') as f:
            f.write(get(url).content)
        return run([
            'sudo', 'tar', '-xvzf', '/tmp/geckodriver.tar.gz',
            '-C', '/usr/local/bin'
        ])

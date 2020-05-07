from lib import download_webpage as dl
from lib import parse_webpage as parser

def process_url(url):
    url_id = dl.download_url(url, 0)
    parser.parse_url(url_id, 0)
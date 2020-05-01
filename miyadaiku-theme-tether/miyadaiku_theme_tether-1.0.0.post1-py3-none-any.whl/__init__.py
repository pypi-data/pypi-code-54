import pkg_resources

from . __version__ import __version__

TETHER_MIN = 'tether.min.js'
TETHER = 'tether.js'
DEST_PATH = '/static/tether/'

def load_package(site):
    f = site.config.getbool('/', 'tether_compressed')
    tether = TETHER_MIN if f else TETHER
    src_path = 'externals/js/'+tether
    
    content = pkg_resources.resource_string(__name__, src_path)
    site.files.add_bytes("binary", DEST_PATH + tether, content )
    site.config.add('/', {'tether_path': DEST_PATH+tether})

    site.add_template_module('tether', 'miyadaiku_theme_tether!macros.html')

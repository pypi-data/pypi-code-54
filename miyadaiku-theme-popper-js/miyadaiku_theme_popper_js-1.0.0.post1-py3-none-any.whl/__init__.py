import pkg_resources

from . __version__ import __version__

POPPER_JS_MIN = 'popper.min.js'
POPPER_JS = 'popper.js'
DEST_PATH = '/static/popper.js/'

def load_package(site):
    f = site.config.getbool('/', 'popper_compressed')
    popper_js = POPPER_JS_MIN if f else POPPER_JS
    src_path = 'externals/'+popper_js
    
    content = pkg_resources.resource_string(__name__, src_path)
    site.files.add_bytes("binary", DEST_PATH + popper_js, content )
    site.config.add('/', {'popper_js_path': DEST_PATH+popper_js})

    site.add_template_module('popper_js', 'miyadaiku_theme_popper_js!macros.html')

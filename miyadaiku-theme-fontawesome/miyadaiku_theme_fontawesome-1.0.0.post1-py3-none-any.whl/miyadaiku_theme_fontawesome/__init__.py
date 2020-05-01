import pkg_resources

__version__ = '1.0.0.post1'

FONTAWESOME_MIN = 'all.min.js'
FONTAWESOME_SHIMS_MIN = 'v4-shims.min.js'
FONTAWESOME = 'all.js'
FONTAWESOME_SHIMS = 'v4-shims.js'
DEST_PATH = '/static/fontawesome/js/'

def load_package(site):
    f = site.config.getbool('/', 'fontawesome_compressed')
    fontawesome = FONTAWESOME_MIN if f else FONTAWESOME

    src_path = 'externals/js/'+fontawesome
    dest_path = DEST_PATH + fontawesome

    content = pkg_resources.resource_string(__name__, src_path)
    site.files.add_bytes("binary", dest_path, content )
    site.config.add('/', {'fontawesome_path': dest_path})

    shims = FONTAWESOME_SHIMS_MIN if f else FONTAWESOME_SHIMS

    shims_path = 'externals/js/'+shims 
    shims_dest = DEST_PATH + shims 

    content = pkg_resources.resource_string(__name__, shims_path)

    site.files.add_bytes("binary", shims_dest , content )
    site.config.add('/', {'fontawesome_shims_path': shims_dest })


    site.add_template_module('fontawesome', 'miyadaiku_theme_fontawesome!macros.html')



import re

from .record import Record


##########
#
#    RGB
#
#########


class Rgb(Record):
    __attributes__ = ['value']

    def __init__(self, value):
        if not re.match(r'^#[0-9a-f]{6}$', value):
            raise ValueError('Bad rgb: %r' % value)
        self.value = value


class MaterialRgb(Rgb):
    __attributes__ = ['name', 'key']

    # https://material.io/design/color/the-color-system.html#tools-for-picking-colors
    values = {
        'Amber': ['#fff8e1', '#ffecb3', '#ffe082', '#ffd54f', '#ffca28', '#ffc107', '#ffb300', '#ffa000', '#ff8f00', '#ff6f00', '#ffe57f', '#ffd740', '#ffc400', '#ffab00'],
        'Blue': ['#e3f2fd', '#bbdefb', '#90caf9', '#64b5f6', '#42a5f5', '#2196f3', '#1e88e5', '#1976d2', '#1565c0', '#0d47a1', '#82b1ff', '#448aff', '#2979ff', '#2962ff'],
        'Blue Grey': ['#eceff1', '#cfd8dc', '#b0bec5', '#90a4ae', '#78909c', '#607d8b', '#546e7a', '#455a64', '#37474f', '#263238'],
        'Brown': ['#efebe9', '#d7ccc8', '#bcaaa4', '#a1887f', '#8d6e63', '#795548', '#6d4c41', '#5d4037', '#4e342e', '#3e2723'],
        'Cyan': ['#e0f7fa', '#b2ebf2', '#80deea', '#4dd0e1', '#26c6da', '#00bcd4', '#00acc1', '#0097a7', '#00838f', '#006064', '#84ffff', '#18ffff', '#00e5ff', '#00b8d4'],
        'Deep Orange': ['#fbe9e7', '#ffccbc', '#ffab91', '#ff8a65', '#ff7043', '#ff5722', '#f4511e', '#e64a19', '#d84315', '#bf360c', '#ff9e80', '#ff6e40', '#ff3d00', '#dd2c00'],
        'Deep Purple': ['#ede7f6', '#d1c4e9', '#b39ddb', '#9575cd', '#7e57c2', '#673ab7', '#5e35b1', '#512da8', '#4527a0', '#311b92', '#b388ff', '#7c4dff', '#651fff', '#6200ea'],
        'Green': ['#e8f5e9', '#c8e6c9', '#a5d6a7', '#81c784', '#66bb6a', '#4caf50', '#43a047', '#388e3c', '#2e7d32', '#1b5e20', '#b9f6ca', '#69f0ae', '#00e676', '#00c853'],
        'Grey': ['#fafafa', '#f5f5f5', '#eeeeee', '#e0e0e0', '#bdbdbd', '#9e9e9e', '#757575', '#616161', '#424242', '#212121'],
        'Indigo': ['#e8eaf6', '#c5cae9', '#9fa8da', '#7986cb', '#5c6bc0', '#3f51b5', '#3949ab', '#303f9f', '#283593', '#1a237e', '#8c9eff', '#536dfe', '#3d5afe', '#304ffe'],
        'Light Blue': ['#e1f5fe', '#b3e5fc', '#81d4fa', '#4fc3f7', '#29b6f6', '#03a9f4', '#039be5', '#0288d1', '#0277bd', '#01579b', '#80d8ff', '#40c4ff', '#00b0ff', '#0091ea'],
        'Light Green': ['#f1f8e9', '#dcedc8', '#c5e1a5', '#aed581', '#9ccc65', '#8bc34a', '#7cb342', '#689f38', '#558b2f', '#33691e', '#ccff90', '#b2ff59', '#76ff03', '#64dd17'],
        'Lime': ['#f9fbe7', '#f0f4c3', '#e6ee9c', '#dce775', '#d4e157', '#cddc39', '#c0ca33', '#afb42b', '#9e9d24', '#827717', '#f4ff81', '#eeff41', '#c6ff00', '#aeea00'],
        'Orange': ['#fff3e0', '#ffe0b2', '#ffcc80', '#ffb74d', '#ffa726', '#ff9800', '#fb8c00', '#f57c00', '#ef6c00', '#e65100', '#ffd180', '#ffab40', '#ff9100', '#ff6d00'],
        'Pink': ['#fce4ec', '#f8bbd0', '#f48fb1', '#f06292', '#ec407a', '#e91e63', '#d81b60', '#c2185b', '#ad1457', '#880e4f', '#ff80ab', '#ff4081', '#f50057', '#c51162'],
        'Purple': ['#f3e5f5', '#e1bee7', '#ce93d8', '#ba68c8', '#ab47bc', '#9c27b0', '#8e24aa', '#7b1fa2', '#6a1b9a', '#4a148c', '#ea80fc', '#e040fb', '#d500f9', '#aa00ff'],
        'Red': ['#ffebee', '#ffcdd2', '#ef9a9a', '#e57373', '#ef5350', '#f44336', '#e53935', '#d32f2f', '#c62828', '#b71c1c', '#ff8a80', '#ff5252', '#ff1744', '#d50000'],
        'Teal': ['#e0f2f1', '#b2dfdb', '#80cbc4', '#4db6ac', '#26a69a', '#009688', '#00897b', '#00796b', '#00695c', '#004d40', '#a7ffeb', '#64ffda', '#1de9b6', '#00bfa5'],
        'Yellow': ['#fffde7', '#fff9c4', '#fff59d', '#fff176', '#ffee58', '#ffeb3b', '#fdd835', '#fbc02d', '#f9a825', '#f57f17', '#ffff8d', '#ffff00', '#ffea00', '#ffd600']
    }
    keys = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900', 'A100', 'A200', 'A400', 'A700']

    def __init__(self, name, key):
        index = self.keys.index(key)
        value = self.values[name][index]
        super(MaterialRgb, self).__init__(value)
        self.name = name
        self.key = key


material = MaterialRgb


#########
#
#   COLOR
#
########


class Color(Record):
    __attributes__ = ['name']

    def __init__(self, name, background=None, border=None, text=None, line=None):
        self.name = name
        self.background = background
        self.border = border
        self.text = text
        self.line = line


BLUE = Color(
    'blue',
    background=material('Blue', '50'),
    border=material('Blue', '100'),
    text=material('Blue', '300'),
    line=material('Blue', '200')
)
GREEN = Color(
    'green',
    background=material('Green', '50'),
    border=material('Green', '100'),
    text=material('Green', '400'),
    line=material('Green', '200')
)
RED = Color(
    'red',
    background=material('Red', '50'),
    border=material('Red', '100'),
    text=material('Red', '300'),
    line=material('Red', '200')
)
ORANGE = Color(
    'orange',
    background=material('Orange', '50'),
    border=material('Orange', '100'),
    text=material('Orange', '300'),
    line=material('Orange', '200')
)
PURPLE = Color(
    'purple',
    background=material('Deep Purple', '50'),
    border=material('Deep Purple', '100'),
    text=material('Deep Purple', '300'),
    line=material('Deep Purple', '200')
)
BROWN = Color(
    'brown',
    background=material('Brown', '50'),
    border=material('Brown', '100'),
    text=material('Brown', '300'),
    line=material('Brown', '200')
)
GREY = Color(
    'grey',
    text=material('Grey', '500'),
    line=material('Grey', '400')
)


#########
#
#    PALETTE
#
#########


class Palette(Record):
    __attributes__ = ['colors', 'cache']

    def __init__(self, colors=None, cache=None):
        if not colors:
            colors = []
        if not cache:
            cache = {}
        self.colors = colors
        for color in colors:
            self.add(color)
        self.cache = cache

    def add(self, color):
        if color not in self.colors:
            self.colors.append(color)

    def get(self, type):
        if type not in self.cache:
            if not self.colors:
                raise ValueError('empty palette')
            index = len(self.cache) % len(self.colors)
            color = self.colors[index]
            self.cache[type] = color
        return self.cache[type]

    def set(self, type, color):
        self.cache[type] = color


PALETTE = Palette([
    BLUE, GREEN, RED,
    ORANGE, PURPLE, BROWN
])


def prepare_color(value, colors=PALETTE.colors):
    if isinstance(value, Color):
        return value

    if isinstance(value, str):
        for color in colors:
            if color.name == value:
                return color
        raise KeyError(value)

    raise TypeError(value)


def palette(*args, **kwargs):
    palette = Palette()
    cache = {}
    for arg in args:
        if isinstance(arg, dict):
            cache.update(arg)
        else:
            color = prepare_color(arg)
            palette.add(color)
    cache.update(kwargs)
    for type, color in cache.items():
        color = prepare_color(color)
        palette.add(color)
        palette.set(type, color)
    return palette

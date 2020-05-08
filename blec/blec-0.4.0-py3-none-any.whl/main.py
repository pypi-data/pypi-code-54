import sys
import re
import argparse
import math

__version__ = '0.4.0'

HEX_COMP3 = re.compile('^[0-9A-Fa-f]{6}(?::\\d+(?:\\.\\d+)?)?$')
HEX_COMP4 = re.compile('^[0-9A-Fa-f]{8}$')
DEC_COMP3 = re.compile('^\\[\\d+(,\\d+){2}\\](?::\\d+(?:\\.\\d+)?)?$')
DEC_COMP4 = re.compile('^\\[\\d+(,\\d+){3}\\]$')

STD_COLORS = {
    'white': (255, 255, 255, 255),
    'black': (0, 0, 0, 255),
}


def from_hex(number):
    return int(number, 16)


def to_argb_hex(color):
    return '{:02x}{:02x}{:02x}{:02x}'.format(color[3], *color[:3])


def to_rgb_hex(color):
    return '{:02x}{:02x}{:02x}'.format(*color[:3])


def to_rgba_hex(color):
    return '{:02x}{:02x}{:02x}{:02x}'.format(*color)


def from_rgb_hex(s):
    r, g, b = s[0:2], s[2:4], s[4:6]
    a = 255
    if len(s) > 6:
        s = s[7:]
        a = int(round(float(s) * 255))
    return tuple(map(from_hex, [r, g, b])) + (a,)


def from_argb_hex(s):
    a, r, g, b = s[0:2], s[2:4], s[4:6], s[6:8]
    return tuple(map(from_hex, [r, g, b, a]))


def from_rgba_hex(s):
    r, g, b, a = s[0:2], s[2:4], s[4:6], s[6:8]
    return tuple(map(from_hex, [r, g, b, a]))


def from_rgb_dec(s):
    end = s.find(']')
    r, g, b = s[1:end].split(',')
    a = 255
    if len(s) > end + 1:
        s = s[end + 2:]
        a = int(round(float(s) * 255))
    return tuple(list(map(int, [r, g, b])) + [a])


def from_rgba_dec(s):
    s = s[1:-1]
    r, g, b, a = s.split(',')
    return tuple(map(int, [r, g, b, a]))


def from_argb_dec(s):
    s = s[1:-1]
    a, r, g, b = s.split(',')
    return tuple(map(int, [r, g, b, a]))


def blend_comp(gamma, dst, src, dst_a, src_a, out_a):
    src = math.pow(src, gamma)
    dst = math.pow(dst, gamma)
    out = (src * src_a + dst * dst_a * (1.0 - src_a)) / out_a
    out = math.pow(out, 1.0 / gamma)
    return clamp(out)


def clamp(value):
    return min(int(round(value)), 255)


def blend(gamma, *colors):
    if not colors:
        return (0, 0, 0, 0)
    dst = colors[0]
    for src in colors[1:]:
        dst_a = dst[3] / 255
        src_a = src[3] / 255
        out_a = src_a + dst_a * (1.0 - src_a)
        if out_a == 0:
            dst = (0, 0, 0, 0)
        else:
            dst = tuple(
                blend_comp(gamma, dst[i], src[i], dst_a, src_a, out_a)
                for i in range(3))
            dst += (clamp(out_a * 255),)
    return dst


def parse_color(argb, str_):
    if str_ in STD_COLORS:
        return STD_COLORS[str_]
    if HEX_COMP3.match(str_):
        return from_rgb_hex(str_)
    if HEX_COMP4.match(str_):
        if argb:
            return from_argb_hex(str_)
        return from_rgba_hex(str_)
    if DEC_COMP3.match(str_):
        return from_rgb_dec(str_)
    if DEC_COMP4.match(str_):
        if argb:
            return from_argb_dec(str_)
        return from_rgba_dec(str_)

    raise Exception('cannot parse color ' + str_)


def parse_and_check_color(argb, str_):
    color = parse_color(argb, str_)
    if any(comp > 255 for comp in color):
        raise Exception('color is out of range ' + str_)
    return color


def process(colors, argb, gamma):
    parsed = [parse_and_check_color(argb, str_) for str_ in colors]
    res = blend(gamma, *parsed)
    if res[3] == 255:
        print(to_rgb_hex(res))
    elif argb:
        print(to_argb_hex(res))
    else:
        print(to_rgba_hex(res))


def main():
    def formatter_class(prog):
        return argparse.RawTextHelpFormatter(
            prog,
            max_help_position=27,
            width=80)
    parser = argparse.ArgumentParser(
        description=(
            'This is a tool to calculate the result of aplha blending process.\n'
            'Enumerate colors from the bottom to the top.'),
        formatter_class=formatter_class)
    parser.add_argument(
        'colors',
        nargs='*',
        metavar='COLOR',
        help=(
            'color in following formats\n\n'
            'RRGGBB\n'
            'RRGGBB:p\n'
            'RRGGBBAA\n'
            '[r,g,b]\n'
            '[r,g,b]:p\n'
            '[r,g,b,a]\n'
            'white or black\n\n'
            'where R, G, B, A are hexadecimal digits\n'
            '      p is opacity in the range [0, 1]\n'
            '      r, g, b, a are are decimal values in the range [0, 255]'))
    parser.add_argument(
        '--argb',
        action='store_true',
        help='use AARRGGBB instead of RRGGBBAA, [a,r,g,b] instead of [r,g,b,a]')
    parser.add_argument(
        '-g',
        '--gamma',
        metavar='GAMMA',
        help='gamma (default: 2.2)',
        default=2.2,
        type=float)
    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='print version and exit')
    args = parser.parse_args()
    if args.version:
        print(__version__)
        sys.exit(0)
    try:
        if args.gamma < 1:
            raise Exception('gamma shoud be higher or equal to 1')
        process(args.colors, args.argb, args.gamma)
    except Exception as err:
        print("error: " + str(err), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

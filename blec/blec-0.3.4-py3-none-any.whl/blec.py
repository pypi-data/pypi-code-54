import sys
import re
import argparse
import math

__version__ = '0.3.1'

COMP3 = re.compile('^#?[0-9A-Fa-f]{6}$')
COMP4 = re.compile('^#?[0-9A-Fa-f]{8}$')

STD_COLORS = {
    'white': (255, 255, 255, 255),
    'black': (0, 0, 0, 255),
}


def from_hex(number):
    return int(number, 16)


def to_argb_hex(color):
    return '#{:02x}{:02x}{:02x}{:02x}'.format(color[3], *color[:3])


def to_rgb_hex(color):
    return '#{:02x}{:02x}{:02x}'.format(*color[:3])


def to_rgba_hex(color):
    return '#{:02x}{:02x}{:02x}{:02x}'.format(*color)


def from_rgb_hex(s):
    s = s.strip().lstrip('#')
    r, g, b = s[0:2], s[2:4], s[4:6]
    return tuple(map(from_hex, [r, g, b])) + (255,)


def from_argb_hex(s):
    s = s.strip().lstrip('#')
    a, r, g, b = s[0:2], s[2:4], s[4:6], s[6:8]
    return tuple(map(from_hex, [r, g, b, a]))


def from_rgba_hex(s):
    s = s.strip().lstrip('#')
    r, g, b, a = s[0:2], s[2:4], s[4:6], s[6:8]
    return tuple(map(from_hex, [r, g, b, a]))


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


def process(colors, argb, gamma):
    parsed = []
    for str_ in colors:
        if str_ in STD_COLORS:
            parsed.append(STD_COLORS[str_])
        elif COMP3.match(str_):
            parsed.append(from_rgb_hex(str_))
        elif COMP4.match(str_):
            if argb:
                parsed.append(from_argb_hex(str_))
            else:
                parsed.append(from_rgba_hex(str_))
        else:
            raise Exception('cannot parse color ' + str_)

    res = blend(gamma, *parsed)
    if res[3] == 255:
        print(to_rgb_hex(res))
    elif argb:
        print(to_argb_hex(res))
    else:
        print(to_rgba_hex(res))


def main():
    def formatter_class(prog):
        return argparse.ArgumentDefaultsHelpFormatter(
            prog,
            max_help_position=27,
            width=80)
    parser = argparse.ArgumentParser(
        description='alpha blending calculator',
        formatter_class=formatter_class)
    parser.add_argument(
        'colors',
        nargs='*',
        metavar='COLOR',
        help='hex colors')
    parser.add_argument(
        '--argb',
        action='store_true',
        help='use ARGB instead of RGBA')
    parser.add_argument(
        '-g',
        '--gamma',
        metavar='GAMMA',
        help='gamma',
        default=2.2,
        type=float)
    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help='use ARGB instead of RGBA')
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

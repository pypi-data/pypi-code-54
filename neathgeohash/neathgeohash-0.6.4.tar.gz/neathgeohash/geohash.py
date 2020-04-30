"""
Copyright (C) 2008 Leonard Norrgard <leonard.norrgard@gmail.com>
Copyright (C) 2015 Leonard Norrgard <leonard.norrgard@gmail.com>

This file is part of Geohash.

Geohash is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Geohash is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public
License along with Geohash.  If not, see
<http://www.gnu.org/licenses/>.
"""
from math import log10
import numpy as np

#  Note: the alphabet in geohash differs from the common base32
#  alphabet described in IETF's RFC 4648
#  (http://tools.ietf.org/html/rfc4648)
__base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
__decodemap = {}
for i in range(len(__base32)):
    __decodemap[__base32[i]] = i
del i
__q = np.array([(2.0 ** 32 / 180.0, 0), (0, 2.0 ** 32 / 360.0)], dtype='float64')
__q.reshape(-1, 2)
__s1 = np.array([(1, 0), (0, 2)])
__s1.dtype = 'uint64'
__sv = (np.arange(12)) * 5
__mask = np.uint64(0x1f)


def decode_exactly(geohash):
    """
    Decode the geohash to its exact values, including the error
    margins of the result.  Returns four float values: latitude,
    longitude, the plus/minus error for latitude (as a positive
    number) and the plus/minus error for longitude (as a positive
    number).
    """
    lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
    lat_err, lon_err = 90.0, 180.0
    is_even = True
    for c in geohash:
        cd = __decodemap[c]
        for mask in [16, 8, 4, 2, 1]:
            if is_even:  # adds longitude info
                lon_err /= 2
                if cd & mask:
                    lon_interval = ((lon_interval[0] + lon_interval[1]) / 2, lon_interval[1])
                else:
                    lon_interval = (lon_interval[0], (lon_interval[0] + lon_interval[1]) / 2)
            else:  # adds latitude info
                lat_err /= 2
                if cd & mask:
                    lat_interval = ((lat_interval[0] + lat_interval[1]) / 2, lat_interval[1])
                else:
                    lat_interval = (lat_interval[0], (lat_interval[0] + lat_interval[1]) / 2)
            is_even = not is_even
    lat = (lat_interval[0] + lat_interval[1]) / 2
    lon = (lon_interval[0] + lon_interval[1]) / 2
    return lat, lon, lat_err, lon_err


def decode(geohash):
    """
    Decode geohash, returning two strings with latitude and longitude
    containing only relevant digits and with trailing zeroes removed.
    """
    lat, lon, lat_err, lon_err = decode_exactly(geohash)
    # Format to the number of decimals that are known
    lats = "%.*f" % (max(1, int(round(-log10(lat_err)))) - 1, lat)
    lons = "%.*f" % (max(1, int(round(-log10(lon_err)))) - 1, lon)
    if '.' in lats: lats = lats.rstrip('0')
    if '.' in lons: lons = lons.rstrip('0')
    return lats, lons


def encode(latitude, longitude, precision=12):
    """
    Encode a position given in float arguments latitude, longitude to
    a geohash which will have the character count precision.
    """
    lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
    geohash = []
    bits = [16, 8, 4, 2, 1]
    bit = 0
    ch = 0
    even = True
    while len(geohash) < precision:
        if even:
            mid = (lon_interval[0] + lon_interval[1]) / 2
            if longitude > mid:
                ch |= bits[bit]
                lon_interval = (mid, lon_interval[1])
            else:
                lon_interval = (lon_interval[0], mid)
        else:
            mid = (lat_interval[0] + lat_interval[1]) / 2
            if latitude > mid:
                ch |= bits[bit]
                lat_interval = (mid, lat_interval[1])
            else:
                lat_interval = (lat_interval[0], mid)
        even = not even
        if bit < 4:
            bit += 1
        else:
            geohash += __base32[ch]
            bit = 0
            ch = 0
    return ''.join(geohash)


# numpy version
def __quantize_points(latlon_mat):
    latlon_mat.reshape(-1, 2)
    a = latlon_mat + np.array((90, 180))
    a = a.dot(__q)
    a = np.floor(a)
    return a


def __encode_into_uint64(quantized_mat):
    """
    Implementation based on "Geohash in Golang Assembly" blog (https://mmcloughlin.com/posts/geohash-assembly)
    by
    :param latlon_mat:
    :return:
    """
    a = np.uint32(quantized_mat)
    a = np.uint64(a)
    a = a.reshape(-1, 2)
    a = np.bitwise_and(np.bitwise_or(a, np.left_shift(a, 16)), 0x0000ffff0000ffff)
    a = np.bitwise_and(np.bitwise_or(a, np.left_shift(a, 8)), 0x00ff00ff00ff00ff)
    a = np.bitwise_and(np.bitwise_or(a, np.left_shift(a, 4)), 0x0f0f0f0f0f0f0f0f)
    a = np.bitwise_and(np.bitwise_or(a, np.left_shift(a, 2)), 0x3333333333333333)
    a = np.bitwise_and(np.bitwise_or(a, np.left_shift(a, 1)), 0x5555555555555555)
    a = np.dot(a, __s1)
    a.dtype = 'uint64'
    g = np.bitwise_or(a[:, 0], a[:, 1])
    g = np.right_shift(g, 4)
    return g


def __encode_base32(g_uint64):
    g = g_uint64
    c11 = np.uint8(np.bitwise_and(np.right_shift([g], 0), __mask))[0]
    c10 = np.uint8(np.bitwise_and(np.right_shift([g], 5), __mask))[0]
    c9 = np.uint8(np.bitwise_and(np.right_shift([g], 10), __mask))[0]
    c8 = np.uint8(np.bitwise_and(np.right_shift([g], 15), __mask))[0]
    c7 = np.uint8(np.bitwise_and(np.right_shift([g], 20), __mask))[0]
    c6 = np.uint8(np.bitwise_and(np.right_shift([g], 25), __mask))[0]
    c5 = np.uint8(np.bitwise_and(np.right_shift([g], 30), __mask))[0]
    c4 = np.uint8(np.bitwise_and(np.right_shift([g], 35), __mask))[0]
    c3 = np.uint8(np.bitwise_and(np.right_shift([g], 40), __mask))[0]
    c2 = np.uint8(np.bitwise_and(np.right_shift([g], 45), __mask))[0]
    c1 = np.uint8(np.bitwise_and(np.right_shift([g], 50), __mask))[0]
    c0 = np.uint8(np.bitwise_and(np.right_shift([g], 55), __mask))[0]
    return np.column_stack((c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11))


def __encode_with_asci(gs_uint8_mat):
    gs_uint8 = np.where(gs_uint8_mat == 0, 48, gs_uint8_mat)  # 0
    gs_uint8 = np.where(gs_uint8 == 1, 49, gs_uint8)  # 1
    gs_uint8 = np.where(gs_uint8 == 2, 50, gs_uint8)  # 2
    gs_uint8 = np.where(gs_uint8 == 3, 51, gs_uint8)  # 3
    gs_uint8 = np.where(gs_uint8 == 4, 52, gs_uint8)  # 4
    gs_uint8 = np.where(gs_uint8 == 5, 53, gs_uint8)  # 5
    gs_uint8 = np.where(gs_uint8 == 6, 54, gs_uint8)  # 6
    gs_uint8 = np.where(gs_uint8 == 7, 55, gs_uint8)  # 7
    gs_uint8 = np.where(gs_uint8 == 8, 56, gs_uint8)  # 8
    gs_uint8 = np.where(gs_uint8 == 9, 57, gs_uint8)  # 9
    gs_uint8 = np.where(gs_uint8 == 10, 98, gs_uint8)  # b
    gs_uint8 = np.where(gs_uint8 == 11, 99, gs_uint8)  # c
    gs_uint8 = np.where(gs_uint8 == 12, 100, gs_uint8)  # d
    gs_uint8 = np.where(gs_uint8 == 13, 101, gs_uint8)  # e
    gs_uint8 = np.where(gs_uint8 == 14, 102, gs_uint8)  # f
    gs_uint8 = np.where(gs_uint8 == 15, 103, gs_uint8)  # g
    gs_uint8 = np.where(gs_uint8 == 16, 104, gs_uint8)  # h
    gs_uint8 = np.where(gs_uint8 == 17, 106, gs_uint8)  # j
    gs_uint8 = np.where(gs_uint8 == 18, 107, gs_uint8)  # k
    gs_uint8 = np.where(gs_uint8 == 19, 109, gs_uint8)  # m
    gs_uint8 = np.where(gs_uint8 == 20, 110, gs_uint8)  # n
    gs_uint8 = np.where(gs_uint8 == 21, 112, gs_uint8)  # p
    gs_uint8 = np.where(gs_uint8 == 22, 113, gs_uint8)  # q
    gs_uint8 = np.where(gs_uint8 == 23, 114, gs_uint8)  # r
    gs_uint8 = np.where(gs_uint8 == 24, 115, gs_uint8)  # s
    gs_uint8 = np.where(gs_uint8 == 25, 116, gs_uint8)  # t
    gs_uint8 = np.where(gs_uint8 == 26, 117, gs_uint8)  # u
    gs_uint8 = np.where(gs_uint8 == 27, 118, gs_uint8)  # v
    gs_uint8 = np.where(gs_uint8 == 28, 119, gs_uint8)  # w
    gs_uint8 = np.where(gs_uint8 == 29, 120, gs_uint8)  # x
    gs_uint8 = np.where(gs_uint8 == 30, 121, gs_uint8)  # y
    gs_uint8 = np.where(gs_uint8 == 31, 122, gs_uint8)  # z
    gs_uint8.reshape(-1, 12)
    gs_uint8.dtype = np.dtype('|S12')
    gs_uint8 = np.squeeze(gs_uint8, axis=1)
    return gs_uint8


# __base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
def fast_encode(lls_list):
    """
    Encode a positions provided as the NumPy array or the list formatted as [[lat, lon], [lat, lon]]
    to an array of geohashes [shape: (1,)] with 12  characters length.

    Comment: fast for a large number of points, do not use it for small values of points!

    :param lls_list: Either np.array or list (i.e. [[lat_1, lon_1], [lat_2, lon_2]]
    :return: ndarray of geohashes with shape: (1,), strings are formated as b'***'
    """
    lls = None
    if not isinstance(lls, (np.ndarray, np.generic)):
        lls = np.array(lls_list)
    else:
        lls = lls_list
    quantized_mat = __quantize_points(lls)
    gs_uint64 = __encode_into_uint64(quantized_mat)
    gs_uint8 = __encode_base32(gs_uint64)
    gs_uint8 = __encode_with_asci(gs_uint8)
    return gs_uint8


def fast_encode_2x_uint32(quantized_mat):
    """
    Encode a set of positions provided as the NumPy array of [uint32, uint32]
    to an array of geohashes [shape: (1,)] with 12  characters length.

    Comment: fast for a large number of points, do not use it for small values of points!

    :param lls_list: Either np.array or list (i.e. [[lat_1, lon_1], [lat_2, lon_2]]
    :return: ndarray of geohashes with shape: (1,), strings are formated as b'***'
    """
    gs_uint64 = __encode_into_uint64(quantized_mat)
    gs_uint8 = __encode_base32(gs_uint64)
    gs_uint8 = __encode_with_asci(gs_uint8)
    return gs_uint8

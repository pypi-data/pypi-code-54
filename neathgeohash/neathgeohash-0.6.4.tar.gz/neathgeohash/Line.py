"""
MIT License

Copyright (c) 2020 Marek Dwulit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
import math as m
import json
from .geohash import fast_encode_2x_uint32, decode_exactly


class Line:
    """
    This Line represents a line segment in (lat, long) coordinate space.
    """

    def __init__(self, lat_start, long_start, lat_end, long_end):
        self.lat_start = lat_start
        self.long_start = long_start
        self.lat_end = lat_end
        self.long_end = long_end
        self.y_s = m.floor(2.0 ** 32 * (self.lat_start + 90.0) / 180.0)
        self.x_s = m.floor(2.0 ** 32 * (self.long_start + 180.0) / 360.0)
        self.y_e = m.floor(2.0 ** 32 * (self.lat_end + 90.0) / 180.0)
        self.x_e = m.floor(2.0 ** 32 * (self.long_end + 180.0) / 360.0)

    @staticmethod
    def __calculate_grid_center(var_uint32, var_step):
        nr_btw = np.uint32(var_step - 1)
        sign_mask = ~nr_btw
        gl_corner = np.uint32(var_uint32) & sign_mask
        g_center = gl_corner + (np.uint32(var_step) // 2 - 1)
        return g_center

    @classmethod
    def __fast_render_line_low(cls, y_s, x_s, y_e, x_e, y_step, x_step):
        x_cs = cls.__calculate_grid_center(x_s, x_step)
        x_ce = cls.__calculate_grid_center(x_e, x_step)
        dx = x_e - x_s
        dy = y_e - y_s
        a = dy / dx
        b = y_s - a * x_s
        x_np = np.arange(x_cs, x_ce + x_step // 2, x_step, dtype=np.uint32)
        if len(x_np) == 0:
            x_np = np.zeros((1,), dtype='uint32')
            x_np[0] = x_s + dx // 2
        else:
            x_np[0] = x_s
            x_np[-1] = x_e
        y_np = x_np * a + b
        line_2uint32 = np.column_stack((y_np, x_np))
        arr = fast_encode_2x_uint32(line_2uint32).astype(str)
        return arr

    @classmethod
    def __fast_render_line_high(cls, y_s, x_s, y_e, x_e, y_step, x_step):
        y_cs = cls.__calculate_grid_center(y_s, y_step)
        y_ce = cls.__calculate_grid_center(y_e, y_step)
        dy = y_e - y_s
        dx = x_e - x_s
        if dy == 0:
            y_np = np.zeros((2,), dtype='uint32')
            y_np[0] = y_s
            y_np[1] = y_e
            x_np = np.zeros((2,), dtype='uint32')
            x_np[0] = x_s
            x_np[1] = x_e
        else:
            a = dx / dy
            b = x_s - a * y_s
            y_np = np.arange(y_cs, y_ce + y_step // 2, y_step, dtype=np.uint32)
            if len(y_np) == 0:
                y_np = np.zeros((1,), dtype='uint32')
                y_np[0] = y_s + dy // 2
            else:
                y_np[0] = y_s
                y_np[-1] = y_e
            x_np = y_np * a + b
        line_2uint32 = np.column_stack((y_np, x_np))
        arr = fast_encode_2x_uint32(line_2uint32).astype(str)
        return arr

    def fast_render_line(self, gh_depth=12):
        """
        Returns set of geohashses approximating a line.
        Warning: The method may produce a large number of geohashes. Use with caution.
        :param gh_depth:
        :return:
        """
        if gh_depth < 12:
            step = 2 ** (((12 - gh_depth) // 2) * 5)
            if gh_depth % 2 == 0:
                step_y = step * 2 ** 2
                step_x = step * 2 ** 2
            else:
                step_y = step * 2 ** 5
                step_x = step * 2 ** 4
        else:
            step_y = step_x = 4

        if abs(self.y_e - self.y_s) < abs(self.x_e - self.x_s):
            if self.x_s < self.x_e:
                ghs_arr = self.__fast_render_line_low(self.y_s, self.x_s, self.y_e, self.x_e, step_y, step_x)
            else:
                ghs_arr = self.__fast_render_line_low(self.y_e, self.x_e, self.y_s, self.x_s, step_y, step_x)
        else:
            if self.y_s < self.y_e:
                ghs_arr = self.__fast_render_line_high(self.y_s, self.x_s, self.y_e, self.x_e, step_y, step_x)
            else:
                ghs_arr = self.__fast_render_line_high(self.y_e, self.x_e, self.y_s, self.x_s, step_y, step_x)
        return ghs_arr

    def get_as_set_of_geohashes_geojson(self, depth=12):
        """
        Converts a list of geohashes representing the line to the geojson feature collection

        :param depth: accuracy for the geohash. Values: 1 to 12
        :return:
        """
        features = []
        ghl = self.fast_render_line(depth)

        for g in ghl:
            gh_decode = decode_exactly(g[0:depth])
            _box = {'s': gh_decode[0] - gh_decode[2],
                    'n': gh_decode[0] + gh_decode[2],
                    'e': gh_decode[1] + gh_decode[3],
                    'w': gh_decode[1] - gh_decode[3]}

            to_append = {
                "type": "Feature",
                "properties": {
                    "geohash": g
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [_box["w"], _box["s"]],
                            [_box["e"], _box["s"]],
                            [_box["e"], _box["n"]],
                            [_box["w"], _box["n"]],
                            [_box["w"], _box["s"]],
                        ]
                    ]
                }
            }
            features += [to_append]

        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }
        return json.dumps(feature_collection)

    def get_as_geometry_linestring_geojson(self, depth=12, with_geohashes=False):
        """
        Returns geojson representing line as the linestring geometry.

        :param with_geohashes: True indicates to put list of geohashes approximating the line. Values: True or False
        :param depth: geohash accuracy
        :return: geojson as string
        """
        if with_geohashes:
            properties = {
                "geohashes": self.fast_render_line(depth).tolist(),
                "geohashes:depth": depth
            }
        else:
            properties = {}

        feature_collection = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [self.long_start, self.lat_start],
                        [self.long_end, self.lat_end]
                    ]
                },
                "properties": properties
            }]
        }
        return json.dumps(feature_collection)

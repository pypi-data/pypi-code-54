"""
Defines GCA Objects

GCA is short for Geometry, Coordinates, Attributes

A GCA object is a collection of geospatial features that are all of the same geometry type (PT', 'LS', 'POLY') with the same attribute fields.

Each GCA object is initiated with:
    Geometry Type: 'PT', 'LS', 'POLY'

    Coordinates: A collection of coordinates grouped by feature.

    Attributes: A 2D list containing the attributes of all features.

"""

import json
import webbrowser
import urllib.parse
from owlet import csv_tools as csvt

__all__ = ["GCA", "from_csv", "valid_geom_types"]

valid_geom_types = ('PT', 'LS', 'POLY')


class GCA:
    """
    Creates aGCA Object

    Attributes
    ----------
    geometry_type : str
        GCA object's geometry type - 'PT', 'LS', 'POLY'
    headers : list of str
        Headers that describe the attributes of each feature in GCA object
    attributes : collection
        The attributes of the GCA object
    coord_sets : collection
        The coordinate sets of the GCA object
    features : collection
        Produces ([Attributes], [Coordinates]) for each feature in GCA object

    Methods
    -------
    egf
        Converts the GCA object to an EGF string.
    gca_str
        GCA object as a string.
    table
        Converts the GCA object to a 2D table
    geo_json
        Converts the GCA object to a GeoJSON Feature Collection
    """

    def __init__(self, geom_type, coords, attrs):
        """
        Initialises a GCA object

        Parameters
        ----------
        geom_type : str
            One of the valid geometry types - 'PT', 'LS', 'POLY'
        coords : collection
            Coordinates of features
        attrs : collection
            2D list of attributes

        """

        if geom_type not in valid_geom_types:
            raise ValueError(f"'{geom_type}' is not a valid geometry type")
        else:
            self.geometry_type = geom_type
        self.headers = attrs[0]
        self.attributes = attrs[1:]
        self.coord_sets = coords
        self.features = list(zip(self.attributes, self.coord_sets))

    def __repr__(self):
        return "Point()"

    def __str__(self):
        description = f"'{self.geometry_type}' GCA object containing {len(self)} feature(s) with the following attributes: {self.attributes}"
        return description

    def __len__(self):
        """
        Counts the number of features contained within the GCA object.

        Returns
        -------
        count : int
            The number of features contained within the GCA object.

        """

        count = len(self.features)

        return count

    def egf(self):
        """
        Converts GCA object to an EGF string.

        Returns
        -------
        str
        """

        def point():
            """
            Converts Point GCA to an EGF string.

            Returns
            -------
            egf_str : str
                Point GCA as an EGF string

            """
            features = self.features

            egf_str = ""

            egf_str += str(self.geometry_type)
            egf_str += "\n" * 4
            egf_str += ', '.join(self.headers)

            for ft in features:
                egf_str += "\n" * 4
                egf_str += ', '.join(ft[0])
                egf_str += "\n"
                egf_str += ', '.join(str(coord) for coord in ft[1])
            egf_str += "\n"

            return egf_str

        def linestring():
            """
            Converts LineString GCA to an EGF string.

            Returns
            -------
            egf_str : str
                LineString GCA as an EGF string

            """

            features = self.features

            egf_str = ""

            egf_str += str(self.geometry_type)
            egf_str += "\n" * 4
            egf_str += ', '.join(self.headers)

            for ft in features:
                egf_str += "\n" * 4
                egf_str += ', '.join(ft[0])

                for coord_set in ft[1]:
                    egf_str += "\n"
                    egf_str += ', '.join(str(coord) for coord in coord_set)

            egf_str += "\n"

            return egf_str

        def polygon():
            """
            Converts Polygon CGA to an EGF string.

            Returns
            -------
            egf_str : str
                Polygon GCA as an EGF string

            """

            egf_str = ""

            egf_str += str(self.geometry_type)
            egf_str += "\n" * 4
            print(self.attributes)
            egf_str += ', '.join(self.attributes)

            for ft in self.features:
                egf_str += "\n" * 4
                egf_str += ', '.join(ft[0])

                for rg_num, ring in enumerate(ft[1]):
                    if rg_num > 0:
                        egf_str += "\n"
                    for coord_set in ring:
                        egf_str += "\n"
                        egf_str += ', '.join(str(coord) for coord in coord_set)

            egf_str += "\n"

            return egf_str

        if self.geometry_type == "PT":
            return point()
        elif self.geometry_type == "LS":
            return linestring()
        elif self.geometry_type == "POLY":
            return polygon()
        else:
            raise ValueError(f"'{self.geometry_type}' is not a valid geometry type")

    def gca_str(self):
        """
        Converts GCA object to a string. Each line is one section of G-C-A

        Returns
        -------
        str
        """

        string = ""
        string += string + str(self.geometry_type)
        string += "\n"
        string += str(self.coord_sets)
        string += "\n"
        string += str([self.headers] + self.attributes)
        string += "\n"

        return string

    def table(self, geometry=True):
        """
        Converts the GCA object to a 2D table

        Parameters
        ----------
        geometry : bool
            True = Include geometry portion of features
            False = Only include attributes of each feature

        Returns
        -------
        csv : collection
            GCA object as a 2D table

        """

        def point():
            if geometry is True:
                csv_table = [self.headers + ["LAT", "LNG", "ELEV"]]
            else:
                csv_table = [self.headers]

            for pt in self.features:
                row = list()
                row.extend(pt[0])

                if geometry is True:
                    lng, lat, z = pt[1]
                    row.extend([lat, lng, z])

                csv_table.append(row)

            return csv_table

        def linestring():
            if geometry is True:
                csv_table = [self.headers + [f"GEOMETRY_{self.geometry_type}"]]
            else:
                csv_table = [self.headers]

            for ls in self.features:
                row = list()
                row.extend(ls[0])

                if geometry is True:
                    row.append(ls[1])

                csv_table.append(row)

            return csv_table

        def polygon():
            if geometry is True:
                csv_table = [self.headers + [f"GEOMETRY_{self.geometry_type}"]]
            else:
                csv_table = [self.headers]

            for poly in self.features:
                row = list()
                row.extend(poly[0])

                if geometry is True:
                    row.append(poly[1])

                csv_table.append(row)

            return csv_table

        if self.geometry_type == "PT":
            return point()
        elif self.geometry_type == "LS":
            return linestring()
        elif self.geometry_type == "POLY":
            return polygon()
        else:
            raise ValueError(f"'{self.geometry_type}' is not a valid geometry type")

    def geo_json(self, visualize=False):
        """
        Converts GCA object to GeoJSON Feature Class.

        Parameters
        ----------
        visualize : bool
            True = Generate GeoJSON string + open with http://geojson.io

        Returns
        -------
        str

        """

        def geo_json_feature_collection():
            """
            Creates a GeoJSON dict from GCA object

            Returns
            -------
            str
            """

            geometry_type = self.geometry_type
            headers = self.headers
            features = self.features

            def feature_init(feature_type):
                """
                Initializes empty GeoJSON feature of a specific type.

                Parameters
                ----------
                feature_type : str
                    PT = Point
                    LS = LineString
                    POLY = Polygon

                Returns
                -------
                dict

                """

                if feature_type == "PT":
                    feature_type = "Point"
                elif feature_type == "LS":
                    feature_type = "LineString"
                elif feature_type == "POLY":
                    feature_type = "Polygon"
                else:
                    raise ValueError(f"'{feature_type}' not recognized as a valid feature type")

                feature = dict()
                feature["type"] = "Feature"
                feature["geometry"] = {}
                feature["geometry"]["type"] = feature_type
                feature["geometry"]["coordinates"] = []
                feature["properties"] = {}

                return feature

            def populate():
                """
                Populates GeoJson Feature Collection with GCA object

                Returns
                -------
                dict

                """

                # initialize feature collection
                fc = dict()
                fc["type"] = "FeatureCollection"
                fc["features"] = list()

                for feature in features:
                    ft_coords = feature[1]
                    ft_attrs = feature[0]

                    json_ft = feature_init(geometry_type)

                    json_ft["geometry"]["coordinates"].extend(ft_coords)
                    json_ft["properties"] = dict(zip(headers, ft_attrs))
                    fc["features"].append(json_ft)

                return fc

            return populate()

        feature_class = geo_json_feature_collection()

        feature_class_string = json.dumps(geo_json_feature_collection())

        if visualize is True:
            url = r"http://geojson.io/#data=data:application/json,"
            url_json = urllib.parse.quote(json.dumps(feature_class, separators=(',', ':')))
            full_url = url + url_json
            webbrowser.open(full_url)

        return feature_class_string


def from_csv(csv_contents, geom_type, keep_geometry=False):
    """

    Parameters
    ----------
    csv_contents : collection
        Contents of a CSV once it has been read
    geom_type : str
        one of the valid GCA geometry types that represents the CSV
    keep_geometry : bool
        True - retains geometry from export as attributes

    Returns
    -------
    GCA

    """
    coordinates = list()
    attributes = list()

    headers = csv_contents[0]

    if geom_type == 'PT':
        coords_index = csvt.col_indexer(headers, ['LNG', 'LAT', 'ELEV'])
        for row in csv_contents[1:]:
            x = row[coords_index[0]]
            y = row[coords_index[1]]
            z = row[coords_index[2]]

            coord_set = [x, y, z]
            coordinates.append(coord_set)

        if keep_geometry is False:
            csv_contents = csvt.column_reducer(csv_contents, ['LNG', 'LAT', 'ELEV'])

            headers = csv_contents[0]

        for row in csv_contents[1:]:
            attributes.append(row)

    elif geom_type == 'LS':
        coords_index = csvt.col_indexer(headers, ["GEOMETRY_LS"])[0]
        for row in csv_contents[1:]:
            coordinates.append(row[coords_index])

        if keep_geometry is False:
            csv_contents = csvt.column_reducer(csv_contents, ["GEOMETRY_LS"])
            headers = csv_contents[0]

        for row in csv_contents[1:]:
            attributes.append(row)

    elif geom_type == 'POLY':
        coords_index = csvt.col_indexer(headers, ["GEOMETRY_POLY"])[0]
        for row in csv_contents[1:]:
            coordinates.append(row[coords_index])

        if keep_geometry is False:
            csv_contents = csvt.column_reducer(csv_contents, ["GEOMETRY_POLY"])

            headers = csv_contents[0]

        for row in csv_contents[1:]:
            attributes.append(row)

    attributes.insert(0, headers)

    gca = GCA(geom_type, coordinates, attributes)

    return gca

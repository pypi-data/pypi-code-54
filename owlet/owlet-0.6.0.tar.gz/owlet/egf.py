"""
Functions that process, validate, and convert EGF files into GCA objects.

"""

from re import search, split
from owlet.file_actions import str_file_read as et
from owlet.gca import GCA, valid_geom_types

__all__ = ["egf_read"]


def validate(egf_str):
    """
    Validates main components of EGF file. This is a first pass validation.

    Parameters
    ----------
    egf_str : str
        The EGF file's contents as a string

    Returns
    -------
    bool
        Only returns True. Exceptions raised as soon a validity test is failed.

    """

    def geometry_type():
        """
        Tests if geometry type declared in EGF is valid.

        """

        geom_type = search(r"\A\w+\b", egf_str).group(0)

        try:
            if geom_type in valid_geom_types:
                pass
            else:
                raise InvalidEGF(f"EGF file needs to be declared as one of the following {valid_geom_types} in the first line")
        except InvalidEGF as err:
            raise err

    def last_line_blank():
        """
        Tests if EGF file ends with a blank line immediately after last coordinate.

        """
        final_two_chars = egf_str[-2:]
        try:
            if final_two_chars[0].isdigit() and final_two_chars[1] == '\n':
                pass
            else:
                raise InvalidEGF("A single blank line is required after final digit of the last coordinate in an EGF file.")
        except InvalidEGF as err:
            raise err

    def section_separators():
        """
        Tests if EGF sections are separated by no more than 4 line breaks (3 blank lines).

        """
        sections = split("\n\n\n\n\n", egf_str)

        try:
            if len(sections) == 1:
                pass
            else:
                raise InvalidEGF("Each section of an EGF file bust be separated by 3 blank lines.")
        except InvalidEGF as err:
            raise err

    def min_sections():
        """
        Tests if EGF has the minimum number of required sections.

        """
        sections = len(split("\n\n\n\n", egf_str))

        try:
            if sections >= 3:
                pass
            else:
                raise InvalidEGF(f"{sections} sections found. Minimum of 3 required - Geometry type, headers, feature")
        except InvalidEGF as err:
            raise err

    def headers():
        """
        Tests if EGF headers section is valid.

        """
        sections = split("\n\n\n\n", egf_str)

        try:
            header_section = sections[1]
            header_row = split("\n", header_section)
            if len(header_row) == 1:
                pass
            else:
                raise InvalidEGF(f"Header section is invalid. Expected one line. Found {len(header_row)}")
        except InvalidEGF as err:
            raise err

    # run tests
    geometry_type()
    last_line_blank()
    section_separators()
    min_sections()
    headers()

    return True


def section_split(egf_str):
    """
    Splits EGF into it's main sections (Geometry Type, Headers, Features)

    Parameters
    ----------
    egf_str : str
        The EGF file's contents as a string

    Returns
    -------
    geom_type : str
    headers : list
    features : collection

    """

    # remove last line (blank)
    egf_str = egf_str[:-1]

    # split into main components (type, headers, and features)
    sections = split("\n\n\n\n", egf_str)

    # type
    geom_type = str(search(r"\A\w+\b", sections[0]).group(0))

    # headers
    headers = split(", ", sections[1])

    # features
    features = list()
    for feature_string in sections[2:]:
        # split feature string at new line. index [0] = attributes | index [1:] = coordinate sets
        feature_split = split("\n", feature_string)
        features.append(feature_split)

    return geom_type, headers, features


def decimal_degree_validate(coordinate):
    """
    Tests if a decimal degree coordinate from an EGF file is valid.

    Parameters
    ----------
    coordinate : str
        example: "-71.070951"

    Returns
    -------
    valid_coordinate : float
        Valid coordinate as a float

    """

    match = search(r"\A[-+]?\d+\.?\d*", coordinate)

    error_msg = f"Coordinate '{coordinate}' is not valid."

    if match is None:
        raise InvalidEGF(error_msg)
    else:
        valid_portion = match.group(0)

    if len(valid_portion) == len(coordinate):
        valid_coordinate = float(valid_portion)
    else:
        raise InvalidEGF(error_msg)

    return valid_coordinate


def attributes_validate(attr_row, headers):
    """
    Test that a feature has the same number of attributes as there are headers in the EGF file.

    Parameters
    ----------
    attr_row : collection
        A row of attributes. Example:  ['attr_1', 'attr2', 'attr_3']
    headers : collection
        A row of headers. Example:  ['hdr_1', 'hdr2', 'hdr_3']

    Returns
    -------
    attr_row : collection
        Returns original attribute row if it is valid

    """

    if len(attr_row) != len(headers):
        raise InvalidEGF("The number of attributes is inconsistent with the defined headers.")

    return attr_row


def point_to_gca(geom_type, headers, features):
    """
    Converts a split 'PT' EGF file into a GCA object.

    inputs are equal to the return of "section_split()"

    Parameters
    ----------
    geom_type : str
        EGF geometry type
    headers : collection
        EGF headers
    features : collection
        EGF features in a list separated by EGF file line.
        Example: [["Feature 1 (Line 1)", "Feature 1 (Line 2)"], ["Feature 2 (Line 1)", "Feature 2 (Line 2)"]]
        Example: [['Boston, MA, USA', '-71.070951, 42.353850, 0'], ["Feature 2 (Line 1)", "Feature 2 (Line 2)"]]

    Returns
    -------
    Point
        GCA Point object
    """

    gca_type = geom_type
    gca_coordinates = list()
    gca_attributes = [headers]

    for ft_num, feature in enumerate(features):
        for ln_num, file_line in enumerate(feature):
            pieces = split(", ", file_line)

            if ln_num == 0:
                gca_attributes.append(attributes_validate(pieces, headers))
            elif len(pieces) == 3:
                coord_set = [decimal_degree_validate(coord) for coord in pieces]
                lat, lng, z = coord_set[0:3]
                xyz_coord_set = [lng, lat, z]
                gca_coordinates.append(xyz_coord_set)
            else:
                raise InvalidEGF(f"Encountered and invalid line: '{file_line}'")

    gca = GCA(gca_type, gca_coordinates, gca_attributes)

    return gca


def linestring_to_gca(geom_type, headers, features):
    """
    Converts a split 'LS' EGF file into a GCA object.

    Inputs are equal to the return of "section_split()"

    Parameters
    ----------
    geom_type : str
        EGF geometry type
    headers : collection
        EGF headers
    features : collection
        EGF features in a list separated by EGF file line.
        Example: [["Feature 1 - Line 1", "Feature 1 - Line 2"], ["Feature 2 - Line 1", "Feature 2 - Line 2"]]

    Returns
    -------
    LineSting
        GCA LineString object

    """

    gca_type = geom_type
    gca_coordinates = list()
    gca_attributes = [headers]

    for ft_num, feature in enumerate(features):
        ls_coord_sets = list()
        for ln_num, file_line in enumerate(feature):
            pieces = split(", ", file_line)

            if ln_num == 0:
                gca_attributes.append(attributes_validate(pieces, headers))
            elif len(pieces) == 3:
                coord_set = [decimal_degree_validate(coord) for coord in pieces]
                lat, lng, z = coord_set[0:3]
                xyz_coord_set = [lng, lat, z]
                ls_coord_sets.append(xyz_coord_set)
            else:
                raise InvalidEGF(f"Encountered and invalid line: '{file_line}'")
        gca_coordinates.append(ls_coord_sets)

    gca = GCA(gca_type, gca_coordinates, gca_attributes)

    return gca


def polygon_to_gca(geom_type, headers, features):
    """
    Converts a split 'POLY' EGF file into a GCA object.

    Inputs are equal to the return of "section_split()"

    Parameters
    ----------
    geom_type : str
        EGF geometry type
    headers : collection
        EGF headers
    features : collection
        EGF features in a list separated by EGF file line.
        Example: [["Feature 1 - Line 1", "Feature 1 - Line 2"], ["Feature 2 - Line 1", "Feature 2 - Line 2"]]

    Returns
    -------
    Polygon
        GCA Polygon object

    """

    gca_type = geom_type
    gca_coordinates = list()
    gca_attributes = [headers]

    polygon_rings = list()
    for ft_num, feature in enumerate(features):
        ring_coord_sets = list()
        feature_line_count = len(feature)

        for ln_num, line in enumerate(feature):
            pieces = split(", ", line)

            if ln_num == 0:
                gca_attributes.append(attributes_validate(pieces, headers))
            elif len(pieces) == 3:
                coord_set = [decimal_degree_validate(coord) for coord in pieces]
                lat, lng, z = coord_set[0:3]
                xyz_coord_set = [lng, lat, z]
                ring_coord_sets.append(xyz_coord_set)
            elif pieces == ['']:
                ring_coord_sets.append(ring_coord_sets[0])
                polygon_rings.append(ring_coord_sets)
                ring_coord_sets = list()
            else:
                raise InvalidEGF(f"Encountered and invalid line: '{line}'")

            # if end of feature
            if (ln_num + 1) == feature_line_count:
                ring_coord_sets.append(ring_coord_sets[0])
                polygon_rings.append(ring_coord_sets)
                gca_coordinates.append(polygon_rings)
                polygon_rings = list()

    gca = GCA(gca_type, gca_coordinates, gca_attributes)

    return gca


def egf_read(file_path):
    """
    Converts an EGF file into the appropriate GCA object.

    Parameters
    ----------
    file_path : str
        Path to file to convert.

    Returns
    -------
    GCA
        GCA object

    """

    content_str = et(file_path)

    if validate(content_str) is True:
        sections = section_split(content_str)

        geom_type = sections[0]

        if geom_type == 'PT':
            return point_to_gca(*sections)
        elif geom_type == 'LS':
            return linestring_to_gca(*sections)
        elif geom_type == 'POLY':
            return polygon_to_gca(*sections)
        else:
            raise InvalidEGF(f"'{geom_type}' not recognized")
    else:
        raise InvalidEGF("EGF file did not convert to GCA")


class InvalidEGF(Exception):
    """
    General exception for invalid EGF files.

    Attributes
    ----------
    message : str
        A message to accompany the exception.

    """

    def __init__(self, message=None):
        if message is None:
            message = "Invalid EGF file"
            super(InvalidEGF, self).__init__(message)
        else:
            self.message = message
    pass

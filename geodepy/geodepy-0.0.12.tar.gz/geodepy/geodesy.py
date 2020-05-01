#!/usr/bin/env python3

"""
Geoscience Australia - Python Geodesy Package
Geodesy Module
"""

from math import degrees, radians, sqrt, sin, cos, tan, asin, acos, atan, atan2
import numpy as np
from geodepy.constants import grs80
from geodepy.convert import geo2grid, grid2geo
from geodepy.statistics import rotation_matrix


def enu2xyz(lat, lon, east, north, up):
    """Convert a column vector in the local reference frame to a column vector
    in the Cartesian reference frame.
    :param lat: latitude in decimal degrees
    :param lon: longitude in decimal degrees
    :param east: in metres
    :param north: in metres
    :param up: in metres
    :return: x, y, z in metres
    """
    rot_matrix = rotation_matrix(lat, lon)
    enu = np.array([[east], [north], [up]])
    xyz = rot_matrix @ enu
    x = xyz[0, 0]
    y = xyz[1, 0]
    z = xyz[2, 0]
    return x, y, z


def xyz2enu(lat, lon, x, y, z):
    """Convert a column vector in the Cartesian reference frame to a column
    vector in the local reference frame.
    :param lat: latitude in decimal degrees
    :param lon: longitude in decimal degrees
    :param x: in metres
    :param y: in metres
    :param z: in metres
    :return: east, north, up in metres
    """
    rot_matrix = rotation_matrix(lat, lon)
    xyz = np.array([[x], [y], [z]])
    enu = rot_matrix.transpose() @ xyz
    east = enu[0, 0]
    north = enu[1, 0]
    up = enu[2, 0]
    return east, north, up


def vincdir(lat1, lon1, azimuth1to2, ell_dist, ellipsoid=grs80):
    """
    Vincenty's Direct Formula
    :param lat1: Latitude of Point 1 (Decimal Degrees)
    :param lon1: Longitude of Point 1 (Decimal Degrees)
    :param azimuth1to2: Azimuth from Point 1 to 2 (Decimal Degrees)
    :param ell_dist: Ellipsoidal Distance between Points 1 and 2 (m)
    :param ellipsoid: Ellipsoid Object
    :return: lat2: Latitude of Point 2 (Decimal Degrees),
             lon2: Longitude of Point 2 (Decimal Degrees),
             azimuth2to1: Azimuth from Point 2 to 1 (Decimal Degrees)

    Code review: 14-08-2018 Craig Harrison
    """

    azimuth1to2 = radians(azimuth1to2)

    # Equation numbering is from the GDA2020 Tech Manual v1.0

    # Eq. 88
    u1 = atan((1 - ellipsoid.f) * tan(radians(lat1)))

    # Eq. 89
    sigma1 = atan2(tan(u1), cos(azimuth1to2))

    # Eq. 90
    alpha = asin(cos(u1) * sin(azimuth1to2))

    # Eq. 91
    u_squared = cos(alpha)**2 \
        * (ellipsoid.semimaj**2 - ellipsoid.semimin**2) \
        / ellipsoid.semimin**2

    # Eq. 92
    a = 1 + (u_squared / 16384) \
        * (4096 + u_squared * (-768 + u_squared * (320 - 175 * u_squared)))

    # Eq. 93
    b = (u_squared / 1024) \
        * (256 + u_squared * (-128 + u_squared * (74 - 47 * u_squared)))

    # Eq. 94
    sigma = ell_dist / (ellipsoid.semimin * a)

    # Iterate until the change in sigma, delta_sigma, is insignificant (< 1e-9)
    # or after 1000 iterations have been completed
    two_sigma_m = 0
    for i in range(1000):

        # Eq. 95
        two_sigma_m = 2*sigma1 + sigma

        # Eq. 96
        delta_sigma = b * sin(sigma) * (cos(two_sigma_m) + (b/4)
                                        * (cos(sigma)
                                           * (-1 + 2 * cos(two_sigma_m)**2)
                                           - (b/6) * cos(two_sigma_m)
                                           * (-3 + 4 * sin(sigma)**2)
                                           * (-3 + 4 * cos(two_sigma_m)**2)))
        new_sigma = (ell_dist / (ellipsoid.semimin * a)) + delta_sigma
        sigma_change = new_sigma - sigma
        sigma = new_sigma

        if abs(sigma_change) < 1e-12:
            break

    # Calculate the Latitude of Point 2
    # Eq. 98
    lat2 = atan2(sin(u1)*cos(sigma) + cos(u1)*sin(sigma)*cos(azimuth1to2),
                 (1 - ellipsoid.f)
                 * sqrt(sin(alpha)**2 + (sin(u1)*sin(sigma)
                        - cos(u1)*cos(sigma)*cos(azimuth1to2))**2))
    lat2 = degrees(lat2)

    # Calculate the Longitude of Point 2
    # Eq. 99
    lon = atan2(sin(sigma)*sin(azimuth1to2),
                cos(u1)*cos(sigma) - sin(u1)*sin(sigma)*cos(azimuth1to2))

    # Eq. 100
    c = (ellipsoid.f/16)*cos(alpha)**2 \
        * (4 + ellipsoid.f*(4 - 3*cos(alpha)**2))

    # Eq. 101
    omega = lon - (1-c)*ellipsoid.f*sin(alpha) \
        * (sigma + c*sin(sigma)*(cos(two_sigma_m) + c*cos(sigma)
                                 * (-1 + 2*cos(two_sigma_m)**2)))

    # Eq. 102
    lon2 = float(lon1) + degrees(omega)

    # Calculate the Reverse Azimuth
    azimuth2to1 = degrees(atan2(sin(alpha), -sin(u1)*sin(sigma)
                          + cos(u1)*cos(sigma)*cos(azimuth1to2))) + 180

    return round(lat2, 11), round(lon2, 11), round(azimuth2to1, 9)


def vincinv(lat1, lon1, lat2, lon2, ellipsoid=grs80):
    """
    Vincenty's Inverse Formula
    :param lat1: Latitude of Point 1 (Decimal Degrees)
    :param lon1: Longitude of Point 1 (Decimal Degrees)
    :param lat2: Latitude of Point 2 (Decimal Degrees)
    :param lon2: Longitude of Point 2 (Decimal Degrees)
    :param ellipsoid: Ellipsoid Object
    :return: ell_dist: Ellipsoidal Distance between Points 1 and 2 (m),
             azimuth1to2: Azimuth from Point 1 to 2 (Decimal Degrees),
             azimuth2to1: Azimuth from Point 2 to 1 (Decimal Degrees)

    Code review: 14-08-2018 Craig Harrison
    """

    # Exit if the two input points are the same
    if lat1 == lat2 and lon1 == lon2:
        return 0, 0, 0

    # Equation numbering is from the GDA2020 Tech Manual v1.0

    # Eq. 71
    u1 = atan((1 - ellipsoid.f) * tan(radians(lat1)))

    # Eq. 72
    u2 = atan((1 - ellipsoid.f) * tan(radians(lat2)))

    # Eq. 73; initial approximation
    lon = radians(lon2 - lon1)
    omega = lon

    # Iterate until the change in lambda, lambda_sigma, is insignificant
    # (< 1e-12) or after 1000 iterations have been completed
    alpha = 0
    sigma = 0
    two_sigma_m = 0
    for i in range(1000):

        # Eq. 74
        sin_sigma = sqrt((cos(u2)*sin(lon))**2
                         + (cos(u1)*sin(u2) - sin(u1)*cos(u2)*cos(lon))**2)

        # Eq. 75
        cos_sigma = sin(u1)*sin(u2) + cos(u1)*cos(u2)*cos(lon)

        # Eq. 76
        sigma = atan2(sin_sigma, cos_sigma)

        # Eq. 77
        alpha = asin((cos(u1)*cos(u2)*sin(lon)) / sin_sigma)

        # Eq. 78
        two_sigma_m = acos(cos(sigma) - 2*sin(u1)*sin(u2) / cos(alpha)**2)

        # Eq. 79
        c = (ellipsoid.f / 16) * cos(alpha)**2 * (4 + ellipsoid.f
                                                  * (4 - 3*cos(alpha)**2))

        # Eq. 80
        new_lon = omega + (1 - c) * ellipsoid.f * sin(alpha) \
            * (sigma + c*sin(sigma) * (cos(two_sigma_m) + c*cos(sigma)
               * (-1 + 2*cos(two_sigma_m)**2)))
        delta_lon = new_lon - lon
        lon = new_lon

        if abs(delta_lon) < 1e-12:
            break

    # Eq. 81
    u_squared = cos(alpha)**2 \
        * (ellipsoid.semimaj**2 - ellipsoid.semimin**2) \
        / ellipsoid.semimin**2

    # Eq. 82
    a = 1 + (u_squared / 16384) \
        * (4096 + u_squared * (-768 + u_squared * (320 - 175 * u_squared)))

    # Eq. 83
    b = (u_squared / 1024) \
        * (256 + u_squared * (-128 + u_squared * (74 - 47 * u_squared)))

    # Eq. 84
    delta_sigma = b*sin(sigma) * (cos(two_sigma_m) + (b / 4)
                                  * (cos(sigma) * (-1 + 2*cos(two_sigma_m)**2)
                                  - (b / 6)*cos(two_sigma_m)
                                  * (-3 + 4*sin(sigma)**2)
                                  * (-3 + 4*cos(two_sigma_m)**2)))
    # Calculate the ellipsoidal distance
    # Eq. 85
    ell_dist = ellipsoid.semimin*a * (sigma - delta_sigma)

    # Calculate the azimuth from point 1 to point 2
    azimuth1to2 = degrees(atan2((cos(u2)*sin(lon)),
                                (cos(u1)*sin(u2)
                                 - sin(u1)*cos(u2)*cos(lon))))

    if azimuth1to2 < 0:
        azimuth1to2 = azimuth1to2 + 360

    # Calculate the azimuth from point 2 to point 1
    azimuth2to1 = degrees(atan2(cos(u1)*sin(lon),
                                (-sin(u1)*cos(u2)
                                 + cos(u1)*sin(u2)*cos(lon)))) + 180

    # Meridian Critical Case Tests
    #if lon1 == lon2 and lat1 > lat2:
    #    azimuth1to2 = 180
    #    azimuth2to1 = 0
    #elif lon1 == lon2 and lat1 < lat2:
    #    azimuth1to2 = 0
    #    azimuth2to1 = 180

    return round(ell_dist, 3), round(azimuth1to2, 9), round(azimuth2to1, 9)


def vincdir_utm(zone1, east1, north1, azimuth1to2, ell_dist, hemisphere1='south', ellipsoid=grs80):
    # Convert utm to geographic
    pt1 = grid2geo(zone1, east1, north1, hemisphere1)
    # Use vincdir
    lat2, lon2, azimuth2to1 = vincdir(pt1[0], pt1[1], azimuth1to2, ell_dist, ellipsoid)
    # Convert geographic to utm
    hemisphere2, zone2, east2, north2, psf2, gc2 = geo2grid(lat2, lon2)
    return hemisphere2, zone2, east2, north2, azimuth2to1


def vincinv_utm(zone1, east1, north1, zone2, east2, north2, hemisphere1='south', hemisphere2='south', ellipsoid=grs80):
    # Convert utm to geographic
    pt1 = grid2geo(zone1, east1, north1, hemisphere1, ellipsoid)
    pt2 = grid2geo(zone2, east2, north2, hemisphere2, ellipsoid)
    # Use vincinv
    return vincinv(pt1[0], pt1[1], pt2[0], pt2[1], ellipsoid)

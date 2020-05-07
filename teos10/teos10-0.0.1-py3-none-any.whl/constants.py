# teos10: unofficial Python implementation of the TEOS-10 properties of water.
# Copyright (C) 2020  Matthew Paul Humphreys  (GNU GPLv3)
"""Constants from IAPWS08 Table 1."""

pnorm = 101_325  # normal pressure in Pa
pstar = 1e8  # reducing pressure in Pa
tzero = 273.15  # Celcius zero point in K
tstar = 40.0  # reducing temperature in K
snorm = 0.035_165_04  # normal salinity in kg/kg
sstar = snorm * 40 / 35  # reducing salinity in kg/kg
Rgas = 8.314_472  # molar gas constant in J/(mol*kg)
saltMass = 31.403_821_8  # molar mass of sea salt in g/mol

# teos10: unofficial Python implementation of the TEOS-10 properties of water.
# Copyright (C) 2020  Matthew Paul Humphreys  (GNU GPLv3)
"""Water properties based on derivatives of Gibbs energy functions."""

from autograd.numpy import sqrt
from autograd import elementwise_grad as egrad
from . import constants, gibbs

default = gibbs.seawater  # which Gibbs energy function to use by default


def dG_dT(gibbsfunc):
    """Function for the first derivative of `gibbsfunc` w.r.t. temperature."""
    return egrad(gibbsfunc, argnum=0)


def dG_dp(gibbsfunc):
    """Function for the first derivative of `gibbsfunc` w.r.t. pressure."""
    return egrad(gibbsfunc, argnum=1)


def dG_dS(gibbsfunc):
    """Function for the first derivative of `gibbsfunc` w.r.t. salinity."""
    return egrad(gibbsfunc, argnum=2)


def d2G_dT2(gibbsfunc):
    """Function for the second derivative of `gibbsfunc` w.r.t. temperature."""
    return egrad(dG_dT(gibbsfunc), argnum=0)


def d2G_dSdp(gibbsfunc):
    """Function for the derivative of `gibbsfunc` w.r.t. salinity and pressure."""
    return egrad(dG_dp(gibbsfunc), argnum=2)


def d2G_dTdp(gibbsfunc):
    """Function for the derivative of `gibbsfunc` w.r.t. temperature and pressure."""
    return egrad(dG_dT(gibbsfunc), argnum=1)


def d2G_dp2(gibbsfunc):
    """Function for the second derivative of `gibbsfunc` w.r.t. pressure."""
    return egrad(dG_dp(gibbsfunc), argnum=1)


def density(*args, gibbsfunc=default):
    """Density (rho) in kg/m**3.  IAPWS09 Table 3 (4)."""
    return 1.0 / dG_dp(gibbsfunc)(*args)


def entropy(*args, gibbsfunc=default):
    """Specific entropy (s) in J/(kg*K).  IAPWS09 Table 3 (5)."""
    return -dG_dT(gibbsfunc)(*args)


def heatCapacity(*args, gibbsfunc=default):
    """Specific isobaric heat capacity (c_p) in J/(kg*K).  IAPWS09 Table 3 (6)."""
    return -args[0] * d2G_dT2(gibbsfunc)(*args)


def enthalpy(*args, gibbsfunc=default):
    """Specific enthalpy (h) in J/kg.  IAPWS09 Table 3 (7)."""
    return gibbsfunc(*args) + args[0] * entropy(*args, gibbsfunc)


def internalEnergy(*args, gibbsfunc=default):
    """Specific internal energy (u) in J/kg.  IAPWS09 Table 3 (8)."""
    return enthalpy(*args, gibbsfunc) - args[1] * dG_dp(gibbsfunc)(*args)


def helmholtzEnergy(*args, gibbsfunc=default):
    """Specific Helmholtz energy (f) in J/kg.  IAPWS09 Table 3 (9)."""
    return gibbsfunc(*args) - args[1] * dG_dp(gibbsfunc)(*args)


def thermalExpansion(*args, gibbsfunc=default):
    """Thermal expansion coefficient (alpha) in 1/K.  IAPWS09 Table 3 (10)."""
    return d2G_dTdp(gibbsfunc)(*args) / dG_dp(gibbsfunc)(*args)


def adiabaticLapseRate(*args, gibbsfunc=default):
    """Isentropic temperature-pressure coefficient, adiabatic lapse rate (beta_s) in
    K/Pa.  IAPWS09 Table 3 (11)."""
    return -d2G_dTdp(gibbsfunc)(*args) / dG_dp(gibbsfunc)(*args)


def isothermalCompressibility(*args, gibbsfunc=default):
    """Isothermal compressibility (kappa_T) in 1/Pa.  IAPWS09 Table 3 (12)."""
    return -d2G_dp2(gibbsfunc)(*args) / dG_dp(gibbsfunc)(*args)


def isenotropicCompressibility(*args, gibbsfunc=default):
    """Isentropic compressibility (kappa_s) in 1/Pa.  IAPWS09 Table 3 (13)."""
    return (
        d2G_dTdp(gibbsfunc)(*args) ** 2
        - d2G_dT2(gibbsfunc)(*args) * d2G_dp2(gibbsfunc)(*args)
    ) / (dG_dp(gibbsfunc)(*args) * dG_dT(gibbsfunc)(*args))


def soundSpeed(*args, gibbsfunc=default):
    """Speed of sound (w) in m/s.  IAPWS09 Table 3 (14)."""
    return dG_dp(gibbsfunc)(*args) * sqrt(
        d2G_dT2(gibbsfunc)(*args)
        / (
            d2G_dTdp(gibbsfunc)(*args) ** 2
            - d2G_dT2(gibbsfunc)(*args) * d2G_dp2(gibbsfunc)(*args)
        )
    )


def relativeChemicalPotential(*args, gibbsfunc=default):
    """Relative chemical potential (mu) in J/kg.  IAPWS08 Table 5 (25)."""
    return dG_dS(gibbsfunc)(*args)


def waterChemicalPotential(*args, gibbsfunc=default):
    """Chemical potential of H2O (mu_W) in J/kg.  IAPWS08 Table 5 (26)."""
    return gibbsfunc(*args) - args[2] * dG_dS(gibbsfunc)(*args)


def saltChemicalPotential(*args, gibbsfunc=default):
    """Chemical potential of sea salt (mu_S) in J/kg.  IAPWS08 Table 5 (27)."""
    return gibbsfunc(*args) + (1 - args[2]) * dG_dS(gibbsfunc)(*args)


def seawaterMolality(sal):
    """Molality of seawater from its salinity."""
    return sal / ((1.0 - sal) * constants.saltMass)


def osmotic(*args, gibbsfunc=default):
    """Osmotic coefficient (phi), dimensionless.  IAPWS08 Table 5 (28)."""
    return -waterChemicalPotential(*args, gibbsfunc=default) / (
        seawaterMolality(args[2]) * constants.Rgas * args[0]
    )


def halineContraction(*args, gibbsfunc=default):
    """Haline contraction coefficient (beta) in kg/kg.  IAPWS08 Table 5 (29)."""
    return -d2G_dSdp(gibbsfunc)(*args) / dG_dp(gibbsfunc)(*args)

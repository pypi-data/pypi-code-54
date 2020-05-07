"""Module to implement semantic versions."""

from typing import Optional

from .semver import SemVer

__all__ = ['SemVer', ]


def validate(version: str) -> bool:
    """Test if string is valid SemVer."""
    return SemVer.validate(version)


def compare(version_a: str, version_b: str) -> int:
    """Compare two version strings."""
    return SemVer.compare(version_a, version_b)


def force(version: str) -> Optional['SemVer']:
    """Attempt to create a SemVer with relaxed parsing rules."""
    return SemVer.force(version)

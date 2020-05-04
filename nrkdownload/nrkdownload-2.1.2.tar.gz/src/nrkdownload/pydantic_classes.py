from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List, Optional


class Image(BaseModel):
    """Generic: An image URL with a corresponding width."""

    url: HttpUrl
    width: int


class Titles(BaseModel):
    """Generic: Title and optional subtitle."""

    class Config:
        """Configuration for this model."""

        anystr_strip_whitespace = True

    title: str
    subtitle: Optional[str] = None


def extract_links_self_href(cls, v):
    """Extract the _links.self.href subfield."""
    if not isinstance(v, dict):
        raise TypeError('Field "_links" type must be dict')
    try:
        href = v["self"]["href"]
    except AttributeError:
        raise ValueError('Field "_links" must contain  ["self"]["href"]')
    return href


class Season(BaseModel):
    """Generic: A season of a series."""

    titles: Titles
    href: str = Field(..., alias="_links")
    sequenceNumber: Optional[int] = None  # Only for sequential series
    name: Optional[str] = None  # Only for news and standard series
    image: Optional[List[Image]] = None
    backdropImage: Optional[List[Image]] = None
    posterImage: Optional[List[Image]] = None

    @validator("name", pre=True, always=True)
    def get_name_from_href(cls, v, values):
        if values["sequenceNumber"] is None:
            return values["href"].split("/")[-1]
        return v

    _get_href = validator("href", always=True, pre=True, allow_reuse=True)(
        extract_links_self_href
    )


class Series(BaseModel):
    """Generic: Information about a series."""

    titles: Titles
    image: Optional[List[Image]] = None
    backdropImage: Optional[List[Image]] = None
    posterImage: Optional[List[Image]] = None
    seasons: Optional[List[Season]] = None

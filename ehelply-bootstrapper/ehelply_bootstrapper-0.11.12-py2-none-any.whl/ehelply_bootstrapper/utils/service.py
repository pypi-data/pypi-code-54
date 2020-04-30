from pydantic import BaseModel
from typing import List


class ServiceMeta(BaseModel):
    name: str
    key: str
    version: str
    summary: str
    authors: List[str]
    author_emails: List[str]


class ServiceStatus(BaseModel):
    health: str = None
    vitals: dict = None
    stats: dict = None
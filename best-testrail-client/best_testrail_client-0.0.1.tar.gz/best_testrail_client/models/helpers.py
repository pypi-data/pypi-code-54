import dataclasses

import typing

from best_testrail_client.custom_types import ModelID
from best_testrail_client.models.basemodel import BaseModel


@dataclasses.dataclass
class Context(BaseModel):
    is_global: bool
    project_ids: typing.Optional[typing.List[ModelID]]


@dataclasses.dataclass
class Options(BaseModel):
    format: str   # noqa: VNE003
    has_actual: bool
    has_expected: bool
    is_required: bool


@dataclasses.dataclass
class FieldConfig(BaseModel):
    id: ModelID  # noqa: A003, VNE003
    context: Context
    options: Options

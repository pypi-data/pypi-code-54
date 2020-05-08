from __future__ import annotations

import dataclasses
import typing

from best_testrail_client.custom_types import ModelID, JsonData
from best_testrail_client.enums import FieldType
from best_testrail_client.models.basemodel import BaseModel
from best_testrail_client.models.helpers import FieldConfig, Context, Options


@dataclasses.dataclass
class ResultField(BaseModel):
    configs: typing.List[FieldConfig]
    display_order: int
    id: ModelID  # noqa: A003, VNE003
    label: str
    name: str
    system_name: str
    type_id: FieldType
    description: typing.Optional[str] = None

    @classmethod
    def from_json(cls: typing.Type[ResultField], data_json: JsonData) -> ResultField:
        data_json = dict(data_json)
        data_json['configs'] = [
            FieldConfig(
                context=Context(
                    is_global=config['context']['is_global'],
                    project_ids=config['context']['project_ids'],
                ),
                options=Options(
                    format=config['options']['format'],
                    has_actual=config['options']['has_actual'],
                    has_expected=config['options']['has_expected'],
                    is_required=config['options']['is_required'],
                ),
                id=config['id'],
            ) for config in data_json.get('configs', [])
        ]
        data_json['type_id'] = FieldType(data_json['type_id'])

        new_instance = ResultField(
            **data_json,
        )

        return new_instance

"""
Contains functions to create an instance of a config class and to load the
configuration files.
"""
import ast
import dataclasses
import logging
from configparser import ConfigParser
from typing import Tuple, Type, Dict, get_origin, Union, get_args, List, Any, Optional

from autoconfiguration.exceptions.data_type_errors import (
    UnableToConvertConfigValueToTypeError,
)
from autoconfiguration.helpers.modify_class import (
    make_singleton,
    add_contains_getattribute_getitem_get_methods_to,
    freeze_class,
    MISSING_VALUE,
)

LOG = logging.getLogger(__name__)


def create_config_instance(config_class: Type, config_files: Tuple[str, ...]):
    """
    Creates an instance of the passed config class with the values of the passed
    config files. The data types of the config class and the types of its attributes
    are validated. The values of the config files are converted to the specified data
    types.

    :param config_class: The class that should be initialized with the values of the
        config files. This class and the types of its attributes have to be dataclasses.
    :param config_files: The files containing the config values for the config class
    :return: The initialized instance of the config class with the values of the
        config files
    """
    config = ConfigParser()
    config.read(config_files)

    sections = {
        _valid_name(section): {
            _valid_name(key): value for key, value in config[section].items()
        }
        for section in config.sections()
    }

    LOG.debug("Generated config with sections: %s", sections)

    return _create_config_class_instance(config_class, sections)


def _valid_name(name: str) -> str:
    return name.replace("-", "_")


def _create_config_class_instance(config_class: Type, sections: Dict):
    instances = []
    for field in dataclasses.fields(config_class):
        instances.append(_get_value_of_field(field, sections))

        add_contains_getattribute_getitem_get_methods_to(
            field.type, sections[field.name] if field.name in sections else {}
        )
        freeze_class(field.type)

    make_singleton(config_class)

    instance = config_class(*instances)
    setattr(instance, "_sections", sections)

    add_contains_getattribute_getitem_get_methods_to(config_class, sections)
    freeze_class(config_class)

    return instance


def _get_value_of_field(field: dataclasses.Field, sections: Dict):
    if field.name in sections:
        values = _get_values_of_sub_fields(field, sections)
        return field.type(*values)
    elif _is_optional(field.type) and not _has_default(field):
        return None
    elif _has_default(field):
        return _get_default(field)
    return MISSING_VALUE


def _get_values_of_sub_fields(field: dataclasses.Field, sections: Dict) -> List[Any]:
    values = []
    for sub_field in dataclasses.fields(field.type):
        if sub_field.name in sections[field.name]:
            values.append(
                _convert_to_correct_type(
                    sections[field.name][sub_field.name], sub_field.type
                )
            )
        elif _is_optional(sub_field.type) and not _has_default(sub_field):
            values.append(None)
        elif _has_default(sub_field):
            values.append(_get_default(sub_field))
        else:
            values.append(MISSING_VALUE)
    return values


def _convert_to_correct_type(value: str, expected_type: Type) -> Any:
    origin_type = get_origin(expected_type)
    if expected_type is str or (
        origin_type is Union and get_args(expected_type)[-1] is str
    ):
        return value

    result = ast.literal_eval(value)
    if (origin_type is None and not isinstance(result, expected_type)) or (
        origin_type is not None and not isinstance(result, origin_type)
    ):
        raise UnableToConvertConfigValueToTypeError(value, expected_type)

    return result


def _is_optional(annotation_type: Type) -> bool:
    return (
        annotation_type is Optional
        or get_origin(annotation_type) is Union
        and get_args(annotation_type)[-1] is type(None)
    )


def _has_default(field: dataclasses.Field) -> bool:
    return (
        field.default is not dataclasses.MISSING
        or field.default_factory is not dataclasses.MISSING
    )


def _get_default(field: dataclasses.Field) -> Any:
    if field.default is not dataclasses.MISSING:
        return field.default
    elif field.default_factory is not dataclasses.MISSING:
        return field.default_factory()

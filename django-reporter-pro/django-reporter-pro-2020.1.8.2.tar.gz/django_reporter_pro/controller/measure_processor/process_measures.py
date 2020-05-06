from django.db.models import F, Sum, Count
from django_reporter_pro.enums.enum_mixin import EnumMixin
from django_reporter_pro.extensions.django.db.models.expressions import ForceF
from django_reporter_pro.extensions.django.db.models.functions.postgresql.timestamp import DateFromTimeStamp
from django_reporter_pro.extensions.django.db.models.sql.jsonb_datastructure import JsonbFunctionTable, JsonbFunction


class AggregateEnum(EnumMixin):
    UN_AGGREGATED = 'unagg'
    COUNT_DISTINCT = 'count'
    COUNT_ALL = 'countall'
    SUM = 'sum'
    AVERAGE = 'average'
    MINIMUM = 'min'
    MAXIMUM = 'max'
    GROUP_DAILY = 'daily'
    GROUP_MONTHLY = 'monthly'
    JSONB_AGGREGATION = 'jsonb_aggregation'
    JSONB_JOIN = 'jsonb_join'


class ProcessMeasure(object):
    @classmethod
    def build_query(cls, model=None, query=None, values=None, measures=None, headers=None):
        annotations = {}
        measured_values = []
        values = [] if not values else values
        headers = [] if not headers else headers
        for key in measures.keys():
            _measure_field = measures.get(key)
            _measure_config = _measure_field.get('_measure_config')
            _measure = _measure_config.get('aggregation')
            # Adding annotations functions
            if str(_measure).startswith('jsonb'):
                _annotation_key = _measure_field.get('query_name') + '_' + _measure
                query, _function = cls.build_jsonb_function(
                    query=query, field=_measure_field, measure_config=_measure_config)
                if _function:
                    annotations[_annotation_key] = _function
                    measured_values.append(_annotation_key)
            else:
                _annotation_key = _measure_field.get('query_name') + '_' + _measure
                annotations[_annotation_key] = cls.build_measure_function(
                    key=_measure_field.get('name'), measure=_measure)
                measured_values.append(_annotation_key)
            # Adding annotations in table values list
            _text = _measure_field.get('verbose_name')
            if _measure_config:
                _text = _measure_config.get('label')
            headers.append({
                "text": _text,
                "value": _annotation_key,
            })
        if values and annotations:
            query = query.annotate(**annotations)
        elif not values and annotations:
            query = query.aggregate(**annotations)
        return headers, query

    @classmethod
    def build_measure_function(cls, key, measure):
        _function = F(key)
        if measure == AggregateEnum.SUM.value:
            _function = Sum(key)
        elif measure == AggregateEnum.COUNT_ALL.value:
            _function = Count(key)
        elif measure == AggregateEnum.GROUP_DAILY.value:
            _function = DateFromTimeStamp(key, 'YYYY-MM-DD')
        elif measure == AggregateEnum.GROUP_MONTHLY.value:
            _function = DateFromTimeStamp(key, 'YYYY-MM')
        return _function

    @classmethod
    def build_jsonb_function(cls, field, query, measure_config):
        _function = None
        _measure = measure_config.get('aggregation')
        if _measure == AggregateEnum.JSONB_JOIN.value:
            _jsonb_config = measure_config.get('jsonb_config')
            _function = ForceF(model=query.model, name=_jsonb_config.get('aggregate_field'),
                               json_field=field.get('query_name'))
            # join jsonb config with query
            _jsonb_columns = [(_column['field'], _column['type']) for _column in _jsonb_config.get('jsonb_columns')]
            join_config = JsonbFunctionTable(
                table_name=query.model._meta.db_table,
                function_name=JsonbFunction.JSONB_TO_RECORDSET,
                field_name='{0}__{1}'.format(
                    field.get('query_name'),
                    '__'.join([_path for _path in _jsonb_config.get('jsonb_path').split(',')])
                ),
                columns=_jsonb_columns,
            )
            query.query.join(join=join_config)
        return query, _function

# Created by shamilsakib at 7/14/2016

from django.core.management.base import BaseCommand
from django.db.models import Count, F
from django_reporter_pro.extensions.django.db.models.expressions import ForceF
from django_reporter_pro.extensions.django.db.models.sql.jsonb_datastructure import JsonbFunctionTable, JsonbFunction

from pocket_survey.survey_backbone.models import QuestionResponseEntity, QuestionGroup


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.requires_model_validation = True

    def handle(self, *args, **options):
        responses = QuestionResponseEntity.objects.filter(
            question_id='48cd9a54-65ee-4809-8d0d-743222a6c17d'
        )
        # Adding extra JOIN
        join_config = JsonbFunctionTable(
            table_name=QuestionResponseEntity._meta.db_table,
            function_name=JsonbFunction.JSONB_TO_RECORDSET,
            field_name='answer__value',
            columns=[('value', 'TEXT'), ('uuid', 'TEXT')]
        )
        responses.query.join(join=join_config)
        # Values
        responses = responses.values('question__title')
        responses = responses.annotate(
            answer_value=ForceF(model=QuestionResponseEntity, name='value', json_field='answer'),
            count=Count(F('uuid')),
        )
        responses = responses.values("question__title", "answer_value", "count")
        print(responses.query)
        for _res in responses:
            print(_res)

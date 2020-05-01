# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-31 15:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0006_auto_20171207_0259'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalOrganization',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('short_name', models.CharField(db_index=True, help_text='Please do not use spaces or special characters. Only allowed special characters are period (.), hyphen (-) and underscore (_).', max_length=255, verbose_name=u'Short Name')),
                ('description', models.TextField(blank=True, null=True)),
                ('logo', models.TextField(blank=True, help_text='Please add only .PNG files for logo images. This logo will be used on certificates.', max_length=255, null=True)),
                ('active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical organization',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]

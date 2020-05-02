# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0004_auto_20170802_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='taggeditem',
            name='created_at',
            field=models.DateTimeField(null=True, db_index=True, auto_now_add=True),
        ),
        migrations.AddField(
            model_name='taggeditem',
            name='created_user',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

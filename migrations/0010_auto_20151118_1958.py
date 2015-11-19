# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0009_checklist_last_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

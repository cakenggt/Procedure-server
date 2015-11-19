# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0008_checklist_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklist',
            name='last_modified',
            field=models.DateField(default=datetime.datetime(2015, 11, 19, 0, 42, 26, 176000, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]

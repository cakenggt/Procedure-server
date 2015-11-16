# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0007_auto_20151116_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklist',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]

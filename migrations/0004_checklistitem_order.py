# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0003_auto_20151116_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistitem',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]

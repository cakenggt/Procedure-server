# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='parent',
            field=models.ForeignKey(to='procedure.Checklist', null=True),
        ),
    ]

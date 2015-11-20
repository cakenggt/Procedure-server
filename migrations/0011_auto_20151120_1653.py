# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0010_auto_20151118_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='procedure.Checklist', null=True),
        ),
    ]

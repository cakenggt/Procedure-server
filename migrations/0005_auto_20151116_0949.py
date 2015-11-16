# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0004_checklistitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='parent',
            field=models.ForeignKey(blank=True, to='procedure.Checklist', null=True),
        ),
    ]

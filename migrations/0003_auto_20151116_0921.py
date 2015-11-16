# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0002_auto_20151116_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistentry',
            name='item',
            field=models.OneToOneField(related_name='entry', primary_key=True, serialize=False, to='procedure.ChecklistItem'),
        ),
    ]

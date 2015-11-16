# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procedure', '0006_checklist_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklistentry',
            name='item',
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='checkable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='checked',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='ChecklistEntry',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('parent', models.ForeignKey(to='procedure.Checklist')),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistEntry',
            fields=[
                ('item', models.OneToOneField(primary_key=True, serialize=False, to='procedure.ChecklistItem')),
                ('checked', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='checklist',
            field=models.ForeignKey(to='procedure.Checklist'),
        ),
    ]

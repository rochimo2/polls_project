# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-16 15:33
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20180205_1756'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='choice',
            managers=[
                ('DoesNotExist', django.db.models.manager.Manager()),
            ],
        ),
    ]

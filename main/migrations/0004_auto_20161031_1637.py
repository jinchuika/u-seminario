# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 16:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20161031_1620'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Trabajador',
            new_name='Perfil',
        ),
    ]

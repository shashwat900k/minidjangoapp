# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-24 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thesocialnetwork', '0003_userfriendship'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfriendship',
            name='identifier',
            field=models.TextField(default='wewdsacddf'),
            preserve_default=False,
        ),
    ]

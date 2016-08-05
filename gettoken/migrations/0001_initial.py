# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-05 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TokenInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('expires', models.CharField(default='-1', max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_name', models.CharField(max_length=255)),
                ('fb_id', models.CharField(max_length=255)),
            ],
        ),
    ]

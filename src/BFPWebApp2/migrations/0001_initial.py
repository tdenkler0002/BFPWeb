# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 23:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('document', models.FileField(blank=True, upload_to='documents')),
            ],
        ),
    ]

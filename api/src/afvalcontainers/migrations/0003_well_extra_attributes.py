# Generated by Django 2.0.1 on 2018-07-16 09:39

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('afvalcontainers', '0002_buurten'),
    ]

    operations = [
        migrations.AddField(
            model_name='well',
            name='extra_attributes',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]

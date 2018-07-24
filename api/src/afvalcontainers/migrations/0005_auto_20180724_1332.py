# Generated by Django 2.0.1 on 2018-07-24 13:32

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('afvalcontainers', '0004_well_geometrie_rd'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('buurtcode', models.CharField(max_length=20)),
                ('stadsdeel', models.CharField(max_length=1)),
                ('stadsdeel_naam', models.CharField(max_length=20)),
                ('straatnaam', models.CharField(max_length=40)),
                ('huisnummer', models.IntegerField(null=True)),
                ('bgt_based', models.NullBooleanField()),
                ('centroid', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('geometrie', django.contrib.gis.db.models.fields.PolygonField(srid=28992)),
                ('extra_attributes', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='well',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wells', to='afvalcontainers.Site'),
        ),
    ]

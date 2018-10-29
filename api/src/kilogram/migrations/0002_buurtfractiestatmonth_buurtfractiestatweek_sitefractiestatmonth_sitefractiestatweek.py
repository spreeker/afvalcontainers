# Generated by Django 2.1.2 on 2018-10-29 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('afvalcontainers', '0011_auto_20181003_0747'),
        ('kilogram', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuurtFractieStatMonth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buurt_code', models.CharField(db_index=True, max_length=4)),
                ('fractie', models.CharField(db_index=True, max_length=20)),
                ('year', models.IntegerField(blank=True, db_index=True, null=True)),
                ('month', models.IntegerField(blank=True, db_index=True, null=True)),
                ('wegingen', models.IntegerField(blank=True, db_index=True, null=True)),
                ('sum', models.IntegerField(blank=True, null=True)),
                ('min', models.IntegerField(blank=True, null=True)),
                ('max', models.IntegerField(blank=True, null=True)),
                ('avg', models.IntegerField(blank=True, null=True)),
                ('stddev', models.IntegerField(blank=True, null=True)),
                ('inhabitants', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BuurtFractieStatWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buurt_code', models.CharField(db_index=True, max_length=4)),
                ('fractie', models.CharField(db_index=True, max_length=20)),
                ('year', models.IntegerField(blank=True, db_index=True, null=True)),
                ('week', models.IntegerField(blank=True, db_index=True, null=True)),
                ('wegingen', models.IntegerField(blank=True, db_index=True, null=True)),
                ('sum', models.IntegerField(blank=True, null=True)),
                ('min', models.IntegerField(blank=True, null=True)),
                ('max', models.IntegerField(blank=True, null=True)),
                ('avg', models.IntegerField(blank=True, null=True)),
                ('stddev', models.IntegerField(blank=True, null=True)),
                ('inhabitants', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SiteFractieStatMonth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fractie', models.CharField(max_length=20)),
                ('month', models.IntegerField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('wegingen', models.IntegerField(blank=True, null=True)),
                ('sum', models.IntegerField(blank=True, null=True)),
                ('min', models.IntegerField(blank=True, null=True)),
                ('max', models.IntegerField(blank=True, null=True)),
                ('avg', models.IntegerField(blank=True, null=True)),
                ('stddev', models.IntegerField(blank=True, null=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthstats', to='afvalcontainers.Site', to_field='short_id')),
            ],
        ),
        migrations.CreateModel(
            name='SiteFractieStatWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fractie', models.CharField(max_length=20)),
                ('week', models.IntegerField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('wegingen', models.IntegerField(blank=True, null=True)),
                ('sum', models.IntegerField(blank=True, null=True)),
                ('min', models.IntegerField(blank=True, null=True)),
                ('max', models.IntegerField(blank=True, null=True)),
                ('avg', models.IntegerField(blank=True, null=True)),
                ('stddev', models.IntegerField(blank=True, null=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekstats', to='afvalcontainers.Site', to_field='short_id')),
            ],
        ),
    ]
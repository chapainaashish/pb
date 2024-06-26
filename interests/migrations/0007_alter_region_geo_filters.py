# Generated by Django 3.2 on 2023-01-29 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0006_region_geo_filters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='geo_filters',
            field=models.CharField(choices=[('WORLD', 'World'), ('COUNTRY', 'Country'), ('REGION', 'Region'), ('CITY', 'City'), ('NONE', 'None')], default='WORLD', max_length=20),
        ),
    ]

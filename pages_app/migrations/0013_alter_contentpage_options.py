# Generated by Django 3.2 on 2023-08-07 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages_app', '0012_auto_20230804_1551'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contentpage',
            options={'ordering': ('types', 'title')},
        ),
    ]

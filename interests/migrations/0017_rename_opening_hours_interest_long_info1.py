# Generated by Django 3.2 on 2023-03-13 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0016_auto_20230313_1133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interest',
            old_name='opening_hours',
            new_name='long_info1',
        ),
    ]

# Generated by Django 3.2 on 2023-01-05 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0005_auto_20221121_2152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='restaurants',
            new_name='interests',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='restaurants',
            new_name='interests',
        ),
        migrations.RenameField(
            model_name='facility',
            old_name='restaurants',
            new_name='interests',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='restaurants',
            new_name='interests',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='restaurants',
            new_name='interests',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='restaurants',
            new_name='interests',
        ),
        migrations.RenameField(
            model_name='sp1',
            old_name='restaurants',
            new_name='interests',
        ),
        migrations.RenameField(
            model_name='world',
            old_name='restaurants',
            new_name='interests',
        ),
    ]

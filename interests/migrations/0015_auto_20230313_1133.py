# Generated by Django 3.2 on 2023-03-13 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interests', '0014_auto_20230313_1130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interest',
            old_name='seating',
            new_name='info4',
        ),
        migrations.AddField(
            model_name='interest',
            name='info4_url',
            field=models.URLField(blank=True),
        ),
    ]
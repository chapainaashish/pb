# Generated by Django 3.2 on 2023-02-20 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0002_post_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billboard',
            name='image',
        ),
    ]
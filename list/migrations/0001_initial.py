# Generated by Django 3.2 on 2022-09-15 18:30

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image
import list.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
                ('cover', models.ImageField(blank=True, max_length=255, upload_to='news')),
                ('display_cover', models.BooleanField(default=True)),
                ('sidebar', models.TextField(blank=True)),
                ('ad_manager', models.TextField(blank=True)),
                ('meta_description', models.TextField(blank=True)),
                ('meta_keywords', models.TextField(blank=True)),
                ('carousel_title', models.CharField(blank=True, max_length=255)),
                ('display_list', models.BooleanField(default=True)),
                ('display_billboard', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('category', models.ForeignKey(default=list.models.get_default_category, on_delete=django.db.models.deletion.CASCADE, related_name='category+', to='list.category')),
                ('list_carousel', models.ManyToManyField(blank=True, related_name='_list_post_list_carousel_+', to='list.Category')),
                ('tags', models.ManyToManyField(blank=True, to='list.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Billboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, max_length=255, upload_to='billboard')),
                ('url', models.URLField(max_length=255)),
                ('display', models.BooleanField(default=True)),
                ('image2', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.FILER_IMAGE_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Autoblogging',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('items', models.IntegerField(default=15)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='list.category')),
            ],
        ),
    ]

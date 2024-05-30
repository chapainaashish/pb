# Generated by Django 3.2 on 2022-09-15 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('interests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WorldRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('order', models.IntegerField(unique=True)),
                ('country', models.ManyToManyField(blank=True, to='filters.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('restaurants', models.ManyToManyField(blank=True, related_name='service_filter', to='interests.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('order', models.IntegerField(unique=True)),
                ('restaurants', models.ManyToManyField(blank=True, related_name='rating_filter', to='interests.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('restaurants', models.ManyToManyField(blank=True, related_name='facility_filter', to='interests.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='CulinaryRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('restaurants', models.ManyToManyField(blank=True, related_name='wineregion_filter', to='interests.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('restaurants', models.ManyToManyField(blank=True, related_name='wine_filter', to='interests.Restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='country',
            name='wine_rg',
            field=models.ManyToManyField(blank=True, to='filters.CulinaryRegion'),
        ),
    ]

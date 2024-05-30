from base import config
from django.db import models
from interests.models import Interest


class World(models.Model):
    name = models.CharField(max_length=255)
    interests = models.ManyToManyField(Interest, blank=True, related_name="world_filter")
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = config.VERBOSE_NAME_WORLD
        verbose_name_plural = config.VERBOSE_NAME_PLURAL_WORLD
        ordering = ['name']


class Country(models.Model):
    name = models.CharField(max_length=255)
    interests = models.ManyToManyField(Interest, blank=True, related_name="country_filter")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = config.VERBOSE_NAME_COUNTRY
        verbose_name_plural = config.VERBOSE_NAME_PLURAL_COUNTRY
        ordering = ['name']


class Region(models.Model):
    name = models.CharField(max_length=255)
    interests = models.ManyToManyField(Interest, blank=True, related_name="region_filter")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = config.VERBOSE_NAME_REGION
        verbose_name_plural = config.VERBOSE_NAME_PLURAL_REGION
        ordering = ['name']


class City(models.Model):
    name = models.CharField(max_length=255)
    interests = models.ManyToManyField(Interest, blank=True, related_name="city_filter")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = config.VERBOSE_NAME_CITY
        verbose_name_plural = config.VERBOSE_NAME_PLURAL_CITY
        ordering = ['name']


class Facility(models.Model):
    name = models.CharField(max_length=255)
    interests = models.ManyToManyField(Interest, blank=True, related_name="facility_filter")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = config.VERBOSE_NAME_FACILITY
        verbose_name_plural = config.VERBOSE_NAME_PLURAL_FACILITY
        ordering = ['name']


class Service(models.Model):
    name = models.CharField(max_length=255)
    interests = models.ManyToManyField(Interest, blank=True, related_name="service_filter")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = config.VERBOSE_NAME_SERVICE
        verbose_name_plural = config.VERBOSE_NAME_PLURAL_SERVICE
        ordering = ['name']


class Rating(models.Model):
    name = models.CharField(max_length=255)
    interests = models.ManyToManyField(Interest, blank=True, related_name="rating_filter")
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = config.VERBOSE_NAME_RATING
        verbose_name_plural = config.VERBOSE_NAME_PLURAL_RATING
        ordering = ['name']


class SP1(models.Model):
    name = models.CharField(max_length=255)
    interests = models.ManyToManyField(Interest, blank=True, related_name="sp1_filter")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = config.VERBOSE_NAME_SP1
        verbose_name_plural = config.VERBOSE_NAME_PLURAL_SP1
        ordering = ['name']


class SP2(models.Model):
    name = models.CharField(max_length=255)
    interests = models.ManyToManyField(Interest, blank=True, related_name="sp2_filter")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = config.VERBOSE_NAME_SP2
        verbose_name_plural = config.VERBOSE_NAME_PLURAL_SP2
        ordering = ['name']


class SP3(models.Model):
    name = models.CharField(max_length=255)
    interests = models.ManyToManyField(Interest, blank=True, related_name="sp3_filter")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = config.VERBOSE_NAME_SP3
        verbose_name_plural = config.VERBOSE_NAME_PLURAL_SP3
        ordering = ['name']

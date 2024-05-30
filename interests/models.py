from base import config
import random
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
import html
from django.core.exceptions import ValidationError
from list.models import Category, Post
from filer.fields.image import FilerImageField
from tinymce import models as tinymce_models

import pages_app.models

User = get_user_model()

GEO_TYPE = (
    ("WORLD", "World"),
    ("COUNTRY", "Country"),
    ("REGION", "Region"),
    ("CITY", "City"),
    ("NONE", "None"),
)


class Region(models.Model):
    geo_link = models.CharField(max_length=255, blank=True, editable=False)
    region_parent = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE)
    geo_filters = models.CharField(max_length=20, choices=GEO_TYPE, default="WORLD")
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = tinymce_models.HTMLField()
    description_on_list = tinymce_models.HTMLField(blank=True)
    thumbnail = FilerImageField(
        null=True, blank=True, on_delete=models.CASCADE, related_name="thumbnail+")
    sidebar = models.TextField(blank=True)
    ad_manager = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    logo_on_navbar = FilerImageField(
        null=True, blank=True, on_delete=models.CASCADE, related_name="logo_on_navbar+")
    list_carousel = models.ManyToManyField(Category, blank=True)
    listing_title1 = models.CharField(max_length=255, blank=True)
    carousel_title = models.CharField(max_length=255, blank=True)
    display_on_navbar = models.BooleanField(default=True)
    display_list = models.BooleanField(default=True, verbose_name="Display Carousel")
    display_billboard = models.BooleanField(default=True)
    navbar_order = models.IntegerField(unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('geo_link',)

    def __str__(self):
        try:
            return self.ordering_name()
        except:
            return self.name

    def ordering_name(self):
        if self.region_parent:
            return f"{self.region_parent.ordering_name()} - {self.name}"
        return self.name
    
    def save(self, *args, **kwargs):
        self.geo_link = self.ordering_name()
        super(Region, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.region_parent is not None:
            return reverse('region', kwargs={'parent': self.region_parent.slug, 'region': self.slug})
        else:
            return reverse('region-without-parent', kwargs={'region': self.slug})    


def create_slug_region(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    rg = Region.objects.filter(slug=slug).order_by("-id")
    pg = pages_app.models.ContentPage.objects.filter(slug=slug).order_by("-id")
    pt = Post.objects.filter(slug=slug).order_by("-date_created")
    if rg.exists() or pg.exists() or pt.exists():
        new_slug = "%s-%s" % (slug, str(random.randrange(1, 1000, 1)))
        return create_slug_region(instance, new_slug=new_slug)
    return slug


def pre_save_receiver_region(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_region(instance)
    if not instance.meta_keywords:
        meta_key = instance.name.lower()
        meta_key += ", " + instance.title.lower()
        instance.meta_keywords = meta_key
    if not instance.meta_description and instance.description:
        meta_desc = instance.description[0:instance.description.find(".")]
        instance.meta_description = html.unescape(strip_tags(meta_desc))


pre_save.connect(pre_save_receiver_region, sender=Region)


class RegionImage(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    region_images = FilerImageField(null=True, blank=True, on_delete=models.CASCADE)


class Interest(models.Model):
    name = models.CharField(max_length=255, blank=True)
    text = tinymce_models.HTMLField(blank=True)
    rating = models.FloatField(default=0)
    custom_overlay = FilerImageField(
        null=True, blank=True, on_delete=models.CASCADE, related_name="custom_overlay+")
    google_map = models.TextField(blank=True)
    info1_url = models.URLField(config.LABEL_INFO1 + "URL", blank=True)
    info1 = models.CharField(config.LABEL_INFO1, max_length=255, blank=True)
    info2_url = models.URLField(config.LABEL_INFO2 + "URL", blank=True)
    info2 = models.CharField(config.LABEL_INFO2, max_length=255, blank=True)
    info3_url = models.URLField(config.LABEL_INFO3 + "URL", blank=True)
    info3 = models.CharField(config.LABEL_INFO3, max_length=255, blank=True)
    info4_url = models.URLField(config.LABEL_INFO4 + "URL", blank=True)
    info4 = models.CharField(config.LABEL_INFO4, max_length=255, blank=True)
    info5_url = models.URLField(config.LABEL_INFO5 + "URL", blank=True)
    info5 = models.CharField(config.LABEL_INFO5, max_length=255, blank=True)
    long_info1 = models.TextField(config.LABEL_LONG_INFO1, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True)
    regions = models.ManyToManyField(
        Region, blank=True, related_name="regions")
    cover = models.ImageField(upload_to="img/%Y/%m/", max_length=255, blank=True)
    cover2 = FilerImageField(null=True, blank=True, on_delete=models.CASCADE)
    sidebar = models.TextField(blank=True)
    ad_manager = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    logo_on_navbar = FilerImageField(
        null=True, blank=True, on_delete=models.CASCADE, related_name="logo_on_navbar+")
    list_carousel = models.ManyToManyField(Category, blank=True)
    carousel_title = models.CharField(max_length=255, blank=True)
    top_slider = models.BooleanField(default=False)
    cover_slider = models.BooleanField(default=False)
    hide_rating = models.BooleanField(default=False)
    display = models.BooleanField(default=False)
    send_email = models.BooleanField(default=True)
    display_list = models.BooleanField(default=True, verbose_name="Display Carousel")
    display_billboard = models.BooleanField(default=True)
    linkup_tags = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=30, blank=True)
    email1 = models.EmailField(blank=True)
    email2 = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    website = models.CharField(max_length=255, blank=True)
    web_text = models.CharField(max_length=255, blank=True)
    website2 = models.CharField(config.LABEL_WEB2_INFO_ADMIN + "URL", max_length=255, blank=True)
    web_text2 = models.CharField(config.LABEL_WEB2_INFO_ADMIN, max_length=255, blank=True)
    number = models.CharField(max_length=20, blank=True)
    isvalidated = models.BooleanField(default=True)
    add_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return config.INTEREST + " : " + self.name

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.user.username
        if not self.email1:
            self.email1 = self.user.email
        super(Interest, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.region.region_parent is not None:
            return reverse('interest-detail', kwargs={'parent': self.region.region_parent.slug, 'region': self.region.slug, 'slug': self.slug})
        else:
            return reverse('interest-detail-without-parent', kwargs={'region': self.region.slug, 'slug': self.slug})

    class Meta:
        verbose_name = config.INTEREST


def create_slug_interest(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Interest.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug_interest(instance, new_slug=new_slug)
    return slug


def pre_save_receiver_interest(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_interest(instance)
    if not instance.meta_keywords:
        meta_key = instance.name.lower()
        if instance.info1:
            meta_key += ", " + instance.info1.lower()
        if instance.info2:
            meta_key += ", " + instance.info2.lower()
        if instance.info4:
            meta_key += ", " + instance.info4.lower()
        instance.meta_keywords = meta_key
    if not instance.meta_description and instance.text:
        meta_desc = instance.text[0:instance.text.find(".")]
        instance.meta_description = html.unescape(strip_tags(meta_desc))


pre_save.connect(pre_save_receiver_interest, sender=Interest)


class TopSliderImage(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    image = FilerImageField(null=True, blank=True, on_delete=models.CASCADE)


class CoverSliderImage(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    image = FilerImageField(null=True, blank=True, on_delete=models.CASCADE)


def review_validator(value):
    if len(value) <= 50:
        raise ValidationError("Enter a minimum of 50 characters")


class ReviewAndRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    recommended = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)], default=10)
    title = models.CharField(max_length=255)
    review = models.TextField(blank=False, validators=[review_validator])
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)], default=10)
    service = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)], default=10)
    cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)], default=10)
    location = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)], default=10)
    sustainability = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)], default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def total_rating(self):
        return round((self.recommended + self.value + self.service + self.cleanliness + self.location + self.sustainability)/6, 2)

    def __str__(self):
        return "Total rating : " + str(self.total_rating()) + " - " + self.title + " - " + str(self.date_created.strftime("%d %b %Y"))


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rr = models.OneToOneField(ReviewAndRating, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=False, validators=[review_validator])
    date_created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " - " + self.title + " - " + self.rr.interest.name

import random
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse
from django.utils.html import strip_tags
import html
from filer.fields.image import FilerImageField
from tinymce import models as tinymce_models

import interests.models


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=200, blank=True)

    def __str__(self):
        return "Category " + self.name


def pre_save_receiver_category(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


pre_save.connect(pre_save_receiver_category, sender=Category)


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "Tag " + self.name


def get_default_category():
    return Category.objects.get(name="Global Travel News").id


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = tinymce_models.HTMLField()
    tags = models.ManyToManyField(Tag, blank=True)
    cover = models.ImageField(
        upload_to="news", blank=True, max_length=255)
    display_cover = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category+", default=get_default_category)
    sidebar = models.TextField(blank=True)
    ad_manager = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    carousel_title = models.CharField(max_length=255, blank=True)
    list_carousel = models.ManyToManyField(Category, blank=True, related_name="list_carousel+")
    display_list = models.BooleanField(default=True, verbose_name="Display Carousel")
    display_billboard = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    date_created = models.DateTimeField(editable=True)

    def __str__(self):
        return "Post : " + self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'category': self.category.slug, 'post': self.slug})


def create_slug_post(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    pt = Post.objects.filter(slug=slug)
    rg = interests.models.Region.objects.filter(slug=slug)
    if pt.exists() or rg.exists():
        new_slug = "%s-%s" % (slug, str(random.randrange(1, 1000, 1)))
        return create_slug_post(instance, new_slug=new_slug)
    return slug


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_post(instance)
    if not instance.meta_keywords:
        meta_key = instance.title.lower()
        instance.meta_keywords = meta_key
    if not instance.meta_description and instance.body:
        meta_desc = instance.body[0:instance.body.find(".")]
        instance.meta_description = html.unescape(strip_tags(meta_desc))


pre_save.connect(pre_save_receiver, sender=Post)


class Autoblogging(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    items = models.IntegerField(default=15)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Billboard(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = FilerImageField(null=True, blank=True, on_delete=models.CASCADE)
    url = models.URLField(max_length=255)
    open_in_new_window = models.BooleanField(default=True)
    display = models.BooleanField(default=True)

    def __str__(self):
        return self.title

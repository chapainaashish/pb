import random
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse
from django.utils.html import strip_tags
import html
from interests.models import Region
from list.models import Category
from filer.fields.image import FilerImageField
from tinymce import models as tinymce_models

TYPE = (
    ("PAGE", "Page"),
    ("FOOTER", "Footer"),
    ("HOME_PAGE", "Home Page"),
    ("SEARCH_PAGE", "Search Page"),
    ("LIST", "List"),
    ("POST", "Post"),
    ("WITHOUT_SIDEBAR", "Without Sidebar"),
    ("LINKUP", "Linkup"),
)

GEO_TYPE = (
    ("WORLD", "World"),
    ("COUNTRY", "Country"),
    ("REGION", "Region"),
    ("CITY", "City"),
    ("NONE", "None"),
)


class ContentPage(models.Model):
    page_parent = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE)
    types = models.CharField(max_length=20, choices=TYPE)
    geo_filters = models.CharField(max_length=20, choices=GEO_TYPE, default="WORLD")
    thumbnail = FilerImageField(null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = tinymce_models.HTMLField(blank=True, verbose_name="Header Content")
    additional_content = tinymce_models.HTMLField(blank=True, verbose_name="Main Content")
    content_on_list = tinymce_models.HTMLField(blank=True, verbose_name="List Content")
    sidebar = models.TextField(blank=True)
    ad_manager = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    logo_on_navbar = FilerImageField(
        null=True, blank=True, on_delete=models.CASCADE, related_name="logo_on_navbar")
    category = models.ManyToManyField(Region, blank=True, verbose_name="List Regions")
    list_section = models.ManyToManyField(Category, blank=True, related_name="list_section+", verbose_name="List Posts")
    list_carousel = models.ManyToManyField(Category, blank=True, related_name="list_carousel+", verbose_name="List Carousel")
    listing_title1 = models.CharField(max_length=255, blank=True, verbose_name="Title Region List")
    show_listing1 = models.BooleanField(default=False, verbose_name="Display List Regions")
    listing_title2 = models.CharField(max_length=255, blank=True, verbose_name="Title Post List")
    show_listing2 = models.BooleanField(default=False, verbose_name="Display List Posts")
    listing_title3 = models.CharField(max_length=255, blank=True, verbose_name="Title Section 3")
    show_listing3 = models.BooleanField(default=False, verbose_name="Display List3")
    carousel_title = models.CharField(max_length=255, blank=True, verbose_name="Title Carousel")
    display_list = models.BooleanField(default=True, verbose_name="Display Carousel")
    display_billboard = models.BooleanField(default=True, verbose_name="Display Billboards")
    navbar_order = models.IntegerField(unique=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)

    class Meta:
        ordering = ('types', 'title',)

    def __str__(self):
        try:
            return self.get_types_display() + " : " + self.title + ', Parent : ' + self.page_parent.title
        except:
            return self.get_types_display() + " : " + self.title

    def get_absolute_url(self):
        if self.types == "HOME_PAGE":
            return reverse('mainpage')
        elif self.types == "SEARCH_PAGE":
            return reverse('searchpage')
        elif self.types == "LIST":
            return reverse('listpage', kwargs={'slug': self.slug})
        elif self.types == "POST":
            return reverse('postpage', kwargs={'slug': self.slug})
        elif self.types == "FOOTER":
            return reverse('footerpage', kwargs={'slug': self.slug})
        elif self.types == "PAGE" or self.types == "WITHOUT_SIDEBAR":
            return reverse('page', kwargs={'slug': self.slug})
        elif self.types == "LINKUP":
            return reverse('linkup', kwargs={'slug': self.slug})


def create_slug_page(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    pg = ContentPage.objects.filter(slug=slug).order_by("-id")
    rg = Region.objects.filter(slug=slug).order_by("-id")
    if pg.exists() or rg.exists():
        new_slug = "%s-%s" % (slug, str(random.randrange(1, 1000, 1)))
        return create_slug_page(instance, new_slug=new_slug)
    return slug


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_page(instance)
    if not instance.meta_keywords:
        meta_key = instance.title.lower()
        instance.meta_keywords = meta_key
    if not instance.meta_description and instance.content:
        meta_desc = instance.content[0:instance.content.find(".")]
        instance.meta_description = html.unescape(strip_tags(meta_desc))


pre_save.connect(pre_save_receiver, sender=ContentPage)


class ImageUpload(models.Model):
    page = models.ForeignKey(ContentPage, on_delete=models.CASCADE)
    image = FilerImageField(null=True, blank=True, on_delete=models.CASCADE)


class Navbar(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(blank=True)
    region = models.ManyToManyField(Region, blank=True)
    page = models.ManyToManyField(ContentPage, blank=True)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.title


class Footer(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(blank=True)
    new_window = models.BooleanField(default=False)
    login_required = models.BooleanField(default=False)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.title


class Sidebar(models.Model):
    sidebar = models.TextField(blank=True)
    ad_manager = models.TextField(blank=True)

    def __str__(self):
        return "Default Sidebar"


class Script(models.Model):
    name = models.CharField(max_length=255)
    script = models.TextField(blank=True)

    def __str__(self):
        return self.name

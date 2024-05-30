from django.contrib import admin
from .models import ContentPage, ImageUpload, Navbar, Footer, Sidebar, Script


class ImageUploadInline(admin.TabularInline):
    model = ImageUpload


class ContentPageAdmin(admin.ModelAdmin):
    inlines = [ImageUploadInline]
    search_fields = ['title', 'content']
    list_filter = ['types']
    fields = ('page_parent', 'types', 'geo_filters', 'thumbnail', 'title', 
    'content', 'additional_content', 'content_on_list', 'sidebar', 
    'ad_manager', 'meta_description', 'meta_keywords', 'logo_on_navbar', 
    ('category', 'listing_title1', 'show_listing1',), 
    ('list_section', 'listing_title2', 'show_listing2',), 
    'listing_title3', 'show_listing3', 
    ('list_carousel', 'carousel_title', 'display_list',), 
    'display_billboard', 'navbar_order', 'slug')


admin.site.register(ContentPage, ContentPageAdmin)
admin.site.register(Navbar)
admin.site.register(Footer)
admin.site.register(Sidebar)
admin.site.register(Script)

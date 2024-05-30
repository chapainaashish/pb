from django.contrib import admin
from .models import RegionImage, Region, Interest, TopSliderImage, CoverSliderImage, ReviewAndRating, Comment
from filters.models import World, Country, Region as RegionFilter, City, Facility, Service, Rating, SP1, SP2, SP3
from import_export.admin import ImportExportModelAdmin
from .resources import InterestResource
from base import config
from .forms import InterestAdminForm


class RegionImageInline(admin.TabularInline):
    model = RegionImage


class RegionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [RegionImageInline]
    readonly_fields = ('slug', 'id', 'geo_link',)


class TopSliderImageInline(admin.TabularInline):
    model = TopSliderImage


class CoverSliderImageInline(admin.TabularInline):
    model = CoverSliderImage


class WorldInline(admin.TabularInline):
    model = World.interests.through
    extra = 0
    verbose_name = config.VERBOSE_NAME_WORLD + " Filter"
    verbose_name_plural = config.VERBOSE_NAME_PLURAL_WORLD + " Filter"


class CountryInline(admin.TabularInline):
    model = Country.interests.through
    extra = 0
    verbose_name = config.VERBOSE_NAME_COUNTRY + " Filter"
    verbose_name_plural = config.VERBOSE_NAME_PLURAL_COUNTRY + " Filter"


class RegionFilterInline(admin.TabularInline):
    model = RegionFilter.interests.through
    extra = 0
    verbose_name = config.VERBOSE_NAME_REGION + " Filter"
    verbose_name_plural = config.VERBOSE_NAME_PLURAL_REGION + " Filter"


class CityInline(admin.TabularInline):
    model = City.interests.through
    extra = 0
    verbose_name = config.VERBOSE_NAME_CITY + " Filter"
    verbose_name_plural = config.VERBOSE_NAME_PLURAL_CITY + " Filter"


class FacilityInline(admin.TabularInline):
    model = Facility.interests.through
    extra = 0
    verbose_name = config.VERBOSE_NAME_FACILITY + " Filter"
    verbose_name_plural = config.VERBOSE_NAME_PLURAL_FACILITY + " Filter"


class ServiceInline(admin.TabularInline):
    model = Service.interests.through
    extra = 0
    verbose_name = config.VERBOSE_NAME_SERVICE + " Filter"
    verbose_name_plural = config.VERBOSE_NAME_PLURAL_SERVICE + " Filter"


class RatingInline(admin.TabularInline):
    model = Rating.interests.through
    extra = 0
    verbose_name = config.VERBOSE_NAME_RATING + " Filter"
    verbose_name_plural = config.VERBOSE_NAME_PLURAL_RATING + " Filter"


class SP1Inline(admin.TabularInline):
    model = SP1.interests.through
    extra = 0
    verbose_name = config.VERBOSE_NAME_SP1 + " Filter"
    verbose_name_plural = config.VERBOSE_NAME_PLURAL_SP1 + " Filter"


class SP2Inline(admin.TabularInline):
    model = SP2.interests.through
    extra = 0
    verbose_name = config.VERBOSE_NAME_SP2 + " Filter"
    verbose_name_plural = config.VERBOSE_NAME_PLURAL_SP2 + " Filter"


class SP3Inline(admin.TabularInline):
    model = SP3.interests.through
    extra = 0
    verbose_name = config.VERBOSE_NAME_SP3 + " Filter"
    verbose_name_plural = config.VERBOSE_NAME_PLURAL_SP3 + " Filter"


class InterestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [TopSliderImageInline, CoverSliderImageInline, 
               WorldInline, CountryInline, RegionFilterInline, CityInline,
               FacilityInline, ServiceInline, RatingInline, SP1Inline, SP2Inline, SP3Inline]
    readonly_fields = ('id', 'add_date', 'mod_date',)
    search_fields = ['name', 'text']
    list_filter = ['display', 'region', 'isvalidated']
    list_display = ('id', 'name', 'add_date', 'mod_date', 'isvalidated',)
    list_display_links = ('id', 'name')
    resource_class = InterestResource
    form = InterestAdminForm

    def has_import_permission(self, request):
        # Only allow superusers to import data
        return request.user.is_superuser

    def has_export_permission(self, request):
        # Only allow superusers to export data
        return request.user.is_superuser

    def get_form(self, request, obj=None, **kwargs):
        form = super(InterestAdmin, self).get_form(request, obj, **kwargs)
        # Only allow superusers to edit user
        if not request.user.is_superuser:
            form.base_fields["user"].disabled = True
        return form


class ReviewAndRatingAdmin(admin.ModelAdmin):
    search_fields = ['title', 'review']
    list_filter = ['approved']


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['title', 'body']
    list_filter = ['approved']


admin.site.register(Region, RegionAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(ReviewAndRating, ReviewAndRatingAdmin)
admin.site.register(Comment, CommentAdmin)

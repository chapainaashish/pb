from django.contrib import admin
from .models import ContactEntry, Subscriber
from import_export.admin import ExportMixin


class SubscriberAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('email', 'name', 'country')
    list_export = ('email', 'name', 'country')


admin.site.register(ContactEntry)
admin.site.register(Subscriber, SubscriberAdmin)

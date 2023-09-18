from django.contrib import admin

from .models import District


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    search_fields = ["name"]

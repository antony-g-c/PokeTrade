from django.contrib import admin

from .models import Card, Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display  = ("card", "seller", "price", "is_active", "created_at")
    list_filter   = ("is_active", "created_at")
    raw_id_fields = ("card", "seller")
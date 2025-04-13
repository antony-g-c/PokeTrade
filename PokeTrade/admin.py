from django.contrib import admin
from .models import Card

class CardAdmin(admin.ModelAdmin):
	list_display = ["owner", "pokemon", "price"]
    search_fields = ["owner", "pokemon"]
    ordering = ("owner", "pokemon", "price")
    list_filter = ["owner"]

admin.site.register(Card, CardAdmin)
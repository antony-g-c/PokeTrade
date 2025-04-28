from django.contrib import admin
from .models import ListingForTrading, OfferTrade

@admin.register(ListingForTrading)
class ListingForTradingAdmin(admin.ModelAdmin):
    list_display = ('listed_card', 'owner', 'is_open', 'date')
    list_filter = ('is_open', 'date')
    search_fields = ('listed_card__name', 'owner__username')
    ordering = ('-date',)

@admin.register(OfferTrade)
class OfferTradeAdmin(admin.ModelAdmin):
    list_display = ('listing', 'offered_by', 'offered_card', 'choice', 'date')
    list_filter = ('choice', 'date')
    search_fields = ('listing__listed_card__name', 'offered_by__username', 'offered_card__name')
    ordering = ('-date',)
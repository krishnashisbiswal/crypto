from django.contrib import admin
from .models import Cryptocurrency, Portfolio, PriceHistory

@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'current_price', 'price_change_24h', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'symbol']
    list_editable = ['current_price', 'is_active']

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'cryptocurrency', 'balance', 'total_invested', 'current_value']
    list_filter = ['cryptocurrency']
    search_fields = ['user__username', 'cryptocurrency__symbol']

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['cryptocurrency', 'price', 'timestamp']
    list_filter = ['cryptocurrency', 'timestamp']
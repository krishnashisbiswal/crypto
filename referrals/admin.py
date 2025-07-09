from django.contrib import admin
from .models import ReferralCommission

@admin.register(ReferralCommission)
class ReferralCommissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'referred_user', 'level', 'amount', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['user__username', 'referred_user__username']

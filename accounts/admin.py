from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'kyc_status', 'referral_code', 'referred_by', 'is_active']
    list_filter = ['kyc_status', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'referral_code']
    actions = ['approve_kyc', 'reject_kyc']
    
    def approve_kyc(self, request, queryset):
        queryset.update(kyc_status='approved')
    approve_kyc.short_description = "Approve KYC"
    
    def reject_kyc(self, request, queryset):
        queryset.update(kyc_status='rejected')
    reject_kyc.short_description = "Reject KYC"
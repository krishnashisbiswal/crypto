from django.contrib import admin
from .models import Deposit

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['user', 'cryptocurrency', 'amount', 'status', 'created_at']
    list_filter = ['status', 'cryptocurrency', 'created_at']
    search_fields = ['user__username', 'transaction_hash']
    actions = ['approve_deposits', 'reject_deposits']
    
    def approve_deposits(self, request, queryset):
        for deposit in queryset.filter(status='pending'):
            # Add approval logic here
            deposit.status = 'approved'
            deposit.save()
    approve_deposits.short_description = "Approve selected deposits"
    
    def reject_deposits(self, request, queryset):
        queryset.update(status='rejected')
    reject_deposits.short_description = "Reject selected deposits"

from django.urls import path
from . import views

app_name = 'deposits'

urlpatterns = [
    path('create/', views.deposit_create, name='deposit_create'),
    path('list/', views.deposit_list, name='deposit_list'),
     path('api/get-wallet-address/<int:coin_id>/', views.get_wallet_address, name='get_wallet_address'),
    # Admin URLs
    path('admin/list/', views.AdminDepositListView.as_view(), name='admin_list'),
    # In your deposits/urls.py
    path('admin/deposits/<int:deposit_id>/approve/', views.admin_approve_deposit, name='admin_approve'),
    path('admin/deposits/<int:deposit_id>/reject/', views.admin_reject_deposit, name='admin_reject'),
    path('admin/list/', views.admin_deposit_list, name='admin_deposit_list'),
]

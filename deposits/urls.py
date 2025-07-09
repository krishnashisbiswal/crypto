from django.urls import path
from . import views

app_name = 'deposits'

urlpatterns = [
    path('create/', views.deposit_create, name='deposit_create'),
    path('list/', views.deposit_list, name='deposit_list'),
    
    # Admin URLs
    path('admin/list/', views.AdminDepositListView.as_view(), name='admin_list'),
    path('admin/approve/<int:deposit_id>/', views.approve_deposit, name='admin_approve'),
    path('<int:deposit_id>/update-status/', views.update_deposit_status, name='update_status'),
]

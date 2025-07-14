from django.urls import path
from . import views

app_name = 'trading'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chart/<int:crypto_id>/', views.price_chart, name='price_chart'),
    
    # Admin URLs
    path('admin/cryptocurrencies/', views.CryptocurrencyListView.as_view(), name='admin_crypto_list'),
    path('admin/cryptocurrencies/add/', views.CryptocurrencyCreateView.as_view(), name='admin_crypto_add'),
    path('admin/cryptocurrencies/<int:crypto_id>/update-price/', views.price_update, name='admin_price_update'),
    path('admin/cryptocurrencies/<int:crypto_id>/toggle/', views.toggle_crypto_status, name='toggle_crypto_status'),
    path('admin/cryptocurrencies/<int:pk>/', views.CryptocurrencyDetailView.as_view(), name='admin_crypto_detail'),
]
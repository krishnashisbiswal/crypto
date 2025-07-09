from django.urls import path
from . import views

app_name = 'referrals'

urlpatterns = [
    path('dashboard/', views.referral_dashboard, name='dashboard'),
]

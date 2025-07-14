
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('terms/', views.terms, name='terms'),
    path('vision/', views.vision, name='vision'),
    path('about/', views.about, name='about'),
    path('revolution/', views.revolution, name='revolution'),
    path('login_home', views.register, name='login_home'),
    path('register/', views.register, name='register'),
    path('login/', views.RoleBasedLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('kyc/', views.kyc_upload, name='kyc_upload'),
]
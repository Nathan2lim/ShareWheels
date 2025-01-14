from django.urls import path
from django.contrib.auth import views as auth_views
from applicompte import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'applicompte'  # Nom du namespace


urlpatterns = [
    path('login/',views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('resend-activation-link/<int:user_id>/', views.resend_activation_link, name='resend_activation_link'),
    path('profile/',views.profile, name = 'profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile')
]


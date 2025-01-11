from django.urls import path
from django.contrib.auth import views as auth_views
from applicompte import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'applicompte'  # Nom du namespace


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name = 'applicompte/login.html'), name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('register/', views.register, name='register'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
]


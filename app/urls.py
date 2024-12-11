from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500
from .views import create_payment


app_name = 'app'  # Nom du namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('reservation/', views.reservation, name='reservation'),
    path('payment/<int:ticket_type_id>/', views.create_payment, name='create_payment'),
    path('succes/', views.succes),
    #path('galeriephoto/', views.galeriephoto),
    
]

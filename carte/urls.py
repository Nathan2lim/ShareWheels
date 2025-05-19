from django.urls import path
from . import views

app_name = 'carte'

urlpatterns = [
    path('', views.festival_map, name='festival_map'),
]
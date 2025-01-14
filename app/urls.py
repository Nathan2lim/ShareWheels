from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500
from .views import create_payment
from django.conf import settings


app_name = 'app'  # Nom du namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('reservation/', views.reservation, name='reservation'),
    path('payment/<int:ticket_type_id>/', views.create_payment, name='create_payment'),
    path('success/', views.success, name='success'),  # Assurez-vous que le nom de la vue est correct
    path('gallery/', views.gallery, name='gallery'),
    path('add-photo/', views.add_photo, name='add_photo'),
    path('add-ticket/', views.add_ticket, name='add_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('add-type-ticket/', views.add_type_ticket, name='add_type_ticket'),
    path('list-type-ticket/', views.list_type_ticket, name='list_type_ticket'),
    path('mytickets/', views.mytickets, name='mytickets'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/<int:ticket_id>/update/', views.ticket_status_update, name='ticket_status_update'),

    #path('galeriephoto/', views.galeriephoto),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib.auth.models import User
from django.db import models

class Photo(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='event_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    localisation = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title if self.title else f"Photo {self.id}"
    
    
class TypeUser(models.Model):
    nom_type = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_type


class Ticket(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0, choices=[(0, 'Non utilisé'), (1, 'Utilisé')])  # 0: Non utilisé, 1: Utilisé
    type_ticket = models.ForeignKey('TypeTicket', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Liaison avec Applicompte
    name = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    qr_code = models.CharField(max_length=255, blank=True, null=True)  # Stocke le lien du QR Code

    def __str__(self):
        return f"Ticket {self.id}"



class TypeTicket(models.Model):
    nom_type = models.CharField(max_length=255)
    tarif = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.nom_type


class Scan(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Liaison avec Applicompte

    def __str__(self):
        return f"Scan {self.id} - {self.timestamp}"

class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=50, unique=True)
    marque = models.CharField(max_length=255, blank=True, null=True)
    modele = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.immatriculation
    

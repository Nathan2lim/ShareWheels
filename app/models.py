from django.contrib.auth.models import User
from django.db import models

class TypeUser(models.Model):
    nom_type = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_type


class Ticket(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    type_ticket = models.ForeignKey('TypeTicket', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Liaison avec Applicompte

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
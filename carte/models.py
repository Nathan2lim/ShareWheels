from django.db import models

class Lieu(models.Model):
    nom = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

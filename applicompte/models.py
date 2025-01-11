from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imatriculation = models.CharField(max_length=7, blank=True, null=True)
    type_user = models.IntegerField(default=0)

    def __str__(self):
        return self.email

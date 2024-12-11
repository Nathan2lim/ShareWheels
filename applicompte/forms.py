from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile  # Import du modèle UserProfile

class UserCreationSW(UserCreationForm):
    num = forms.IntegerField(label="Numéro spécifique")  # Champ personnalisé

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'num')

    def save(self, commit=True):
        user = super().save(commit=False)  # Appeler la méthode parente pour créer l'utilisateur
        if commit:
            user.save()  # Sauvegarder l'utilisateur
            # Créer un profil utilisateur associé
            UserProfile.objects.create(user=user, num=self.cleaned_data['num'])
        return user

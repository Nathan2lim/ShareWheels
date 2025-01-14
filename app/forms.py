from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image', 'author','localisation','description']  # Champs à inclure dans le formulaire


from django import forms
from .models import Ticket, TypeTicket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['type_ticket','name', 'prenom']  # Seul le type de ticket est sélectionné par l'utilisateur
        
class TypeTicketForm(forms.ModelForm):
    class Meta:
        model = TypeTicket
        fields = ['nom_type', 'tarif', 'description', 'image']  # Champs modifiables
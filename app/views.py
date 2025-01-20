from app.models import *
from django.shortcuts import get_object_or_404, render,redirect
from django.conf import settings
from .forms import PhotoForm
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Ticket, TypeTicket
from .forms import TicketForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import TypeTicket
from .forms import TypeTicketForm
import qrcode
from io import BytesIO
import base64

import stripe
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    return render(request, 'app/home.html')

def reservation(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour réserver un ticket.")
        return redirect('applicompte:login')
    
    lesTickets = TypeTicket.objects.all()
    return render(request, 'app/reservation.html', {'tickets': lesTickets})

def create_payment(request, ticket_type_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour réserver un ticket.")
        return redirect('applicompte:login')
    
    # Récupère le type de ticket à payer
    ticket_type = get_object_or_404(TypeTicket, id=ticket_type_id)

    # Crée une session de paiement Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': ticket_type.nom_type,
                    },
                    'unit_amount': int(ticket_type.tarif * 100),  # Convertir en centimes
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url = f"{reverse('success')}?ticket_type_id={ticket_type.id}",
        cancel_url=f"{reverse('gallery')},
    )

    # Redirige vers Stripe Checkout
    return redirect(session.url, code=303)



def success(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour réserver un ticket.")
        return redirect('applicompte:login')
    
    # Récupère l'utilisateur connecté et le type de ticket
    user = request.user
    ticket_type_id = request.GET.get('ticket_type_id')

    if not ticket_type_id:
        return redirect('app:ticket_list')  # Redirige si le ticket_type_id est manquant

    ticket_type = get_object_or_404(TypeTicket, id=ticket_type_id)

    # Crée un ticket sans QR code d'abord
    ticket = Ticket.objects.create(
        type_ticket=ticket_type,
        user=user,
        status="0"
    )

    # Met à jour le QR code après avoir créé le ticket
    ticket.qr_code = f"https://sherwheels.fr/ticket/{ticket.id}/update"
    ticket.save()

    # Récupère tous les tickets de l'utilisateur pour l'affichage
    tickets = Ticket.objects.filter(user=user)

    return render(request, 'app/success.html', {'tickets': tickets})

def cancel(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour réserver un ticket.")
        return redirect('applicompte:login')
    
    return render(request, 'app/cancel.html')

def gallery(request):
    photos = Photo.objects.all()  # Récupère toutes les photos
    return render(request, 'app/gallery.html', {'photos': photos})

def add_photo(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour réserver un ticket.")
        return redirect('applicompte:login')
    if not request.user.is_staff:
        messages.warning(request, "Vous devez être un utilisateur premium pour ajouter une photo.")
        return redirect('app:gallery')
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "La photo a été ajoutée avec succès.")
            return redirect('app:gallery')  # Redirige vers la galerie après l'ajout
    else:
        form = PhotoForm()
    
    return render(request, 'app/add_photo.html', {'form': form})

def add_ticket(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour réserver un ticket.")
        return redirect('applicompte:login')
    if not request.user.is_staff:
        messages.warning(request, "Vous devez être un utilisateur premium pour ajouter un ticket.")
        return redirect('app:ticket_list')
    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Associe le ticket à l'utilisateur connecté            
            # Génère un lien unique pour le QR code
            ticket.qr_code = f"https://https://sherwheels.fr/ticket/{ticket.id}/update"  # Remplacez `example.com` par votre domaine
            
            ticket.save()
            messages.success(request, "Votre ticket a été ajouté avec succès.")
            return redirect('app:ticket_list')  # Redirige vers une liste de tickets ou une autre page
    else:
        form = TicketForm()
    
    return render(request, 'app/add_ticket.html', {'form': form})


def ticket_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour réserver un ticket.")
        return redirect('applicompte:login')
    
    if not request.user.is_staff:
        messages.warning(request, "Vous devez être un utilisateur premium pour voir les tickets.")
        return redirect('app:home')
    
    tickets = Ticket.objects.all()  # Affiche uniquement les tickets de l'utilisateur connecté
    return render(request, 'app/myticket.html', {'tickets': tickets})

def add_type_ticket(request):
    
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour réserver un ticket.")
        return redirect('applicompte:login')
    
    if not request.user.is_staff:
        messages.warning(request, "Vous devez être un utilisateur premium pour ajouter un type de ticket.")
        return redirect('app:list_type_ticket')
    
    if request.method == 'POST':
        form = TypeTicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Le type de ticket a été ajouté avec succès.")
            return redirect('app:list_type_ticket')  # Redirige vers la liste des types de tickets
    else:
        form = TypeTicketForm()
    return render(request, 'app/add_type_ticket.html', {'form': form})

def list_type_ticket(request):
    
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour réserver un ticket.")
        return redirect('applicompte:login')
    
    if not request.user.is_staff:
        messages.warning(request, "Vous devez être un utilisateur premium pour voir les types de tickets.")
        return redirect('app:home')
    
    types = TypeTicket.objects.all()  # Récupère tous les types de tickets
    return render(request, 'app/list_type_ticket.html', {'types': types})


def mytickets(request):
    
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour voir vos tickets.")
        return redirect('applicompte:login')
    
    # Récupère tous les types de tickets (utile pour les afficher ou les filtrer)
    types = TypeTicket.objects.all()
    
    # Récupère les tickets de l'utilisateur connecté
    tickets = Ticket.objects.filter(user=request.user)
    
    return render(request, 'app/myticket.html', {'types': types, 'tickets': tickets})

def ticket_detail(request, ticket_id):
    
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour voir vos tickets.")
        return redirect('applicompte:login')
    
    if not request.user.id == Ticket.objects.get(id=ticket_id).user_id:
        messages.warning(request, "Vous ne pouvez pas voir les tickets des autres utilisateurs.")
        return redirect('app:mytickets') 
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Générer le QR code dynamiquement
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(ticket.qr_code)  # Encode l'URL stockée dans `qr_code`
    qr.make(fit=True)
    
    # Convertir l'image en base64
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return render(request, 'app/ticket_detail.html', {'ticket': ticket, 'qr_code_base64': qr_code_base64})

def ticket_status_update(request, ticket_id):
    
    if not request.user.is_authenticated:
        messages.warning(request, "Vous devez vous connecter pour voir vos tickets.")
        return redirect('applicompte:login')
    
    if not request.user.userprofile.type_user == 1 or not request.user.is_staff:
        messages.warning(request, "Vous devez être un utilisateur premium pour mettre à jour le statut d'un ticket.")
        return redirect('app:mytickets')
    
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        # Change le statut en fonction de l'action
        if action == "down":
            ticket.status = "Invalide"  # Statut pour un ticket utilisé
        elif action == "up":
            ticket.status = "Utilisable"  # Statut pour un ticket réactivé
        else:
            messages.error(request, "Action non valide.")
            return render(request, 'app/ticket_status_update.html', {'ticket': ticket})

        # Sauvegarde les modifications
        ticket.save()
        messages.success(request, f"Le statut du ticket a été mis à jour : {ticket.status}")
        return render(request, 'app/ticket_status_update.html', {'ticket': ticket})

    return render(request, 'app/ticket_status_update.html', {'ticket': ticket})

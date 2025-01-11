from app.models import *
from django.shortcuts import get_object_or_404, render,redirect
from django.conf import settings
import stripe
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    return render(request, 'app/home.html')

def reservation(request):
    lesTickets = TypeTicket.objects.all()
    return render(request, 'app/reservation.html', {'tickets': lesTickets})

def create_payment(request, ticket_type_id):

    # Récupérer le ticket sélectionné
    ticket = get_object_or_404(TypeTicket, id=ticket_type_id)

    # Créer une session de paiement Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': ticket.nom_type,
                    },
                    'unit_amount': int(ticket.tarif * 100),  # Convertir en centimes
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='http://127.0.0.1:8000/succes/',
        cancel_url='http://127.0.0.1:8000/cancel/',
    )
    Ticket.objects.create(type_ticket=ticket, user=request.user, status='Confirmé') 
    # Rediriger directement vers Stripe Checkout
    return redirect(session.url, code=303)

def succes(request):
    # on recupere le nom de l'utilisateur et on affiche toute ces reservations
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    return render(request, 'app/succes.html', {'tickets': tickets})

def cancel(request):
    return render(request, 'app/cancel.html')
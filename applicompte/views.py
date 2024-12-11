from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from app.models import *
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.urls import reverse
from .forms import *


# Create your views here.
def connexion(request):

    if request.user.is_authenticated:
            return redirect('app:home')
    else:
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=usr, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('app:home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return redirect('login')

def deconnexion(request):
    logout(request)
    return render(
        request,
        'applicompte/logout.html'
    )

def inscription(request):
    if request.method == 'POST':
        form = UserCreationSW(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique après l'inscription
            return redirect('app:home')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserCreationSW()
    return render(request, 'applicompte/inscription.html', {'form': form})

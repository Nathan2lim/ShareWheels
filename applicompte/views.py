from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from app.models import *
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.urls import reverse
from .forms import *


# Create your views here.
def login(request):

    if request.user.is_authenticated:
        return redirect('app:home')
    else:
        usr = request.POST.get('username') #todo email instead of username
        pwd = request.POST.get('password')
        user = authenticate(request, username=usr, password=pwd)
        if user is not None:
            django_login(request, user)
            return redirect('app:home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return redirect('login')

def logout(request): 
    django_logout(request)
    
    return render(
        request,
        'applicompte/logout.html'
    )

def forgetpassword(request):
    #? todo if connected not needed (use editpassword instead or disconnect before)
    
    
    return render(
        request,
        'applicompte/forgetpassword.html'
    )

def register(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        form = UserCreationSW(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)  # Connexion automatique après l'inscription
            return redirect('app:home')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserCreationSW()
    return render(request, 'applicompte/register.html', {'form': form})
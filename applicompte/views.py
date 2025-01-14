import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_http_methods

from app.models import *
from .forms import *

def login(request):

    print("login")
    if request.user.is_authenticated:
        messages.info(request, "Vous êtes déjà connecté.")
        print("already connected")
        return redirect('app:home')

    if request.method == 'POST':
        email = request.POST.get('username')  # Champ email
        pwd = request.POST.get('password')   # Champ mot de passe
        print("try to connect")
        
        if not email or not pwd:
            messages.error(request, "Veuillez remplir tous les champs.")
            print("empty fields")
        else:
            try:
                user = User.objects.get(email=email)
                print("user found")
                if(user.is_active == False):
                     # Lien pour renvoyer l'activation
                    resend_link = reverse('applicompte:resend_activation_link', args=[user.id])
                    messages.error(
                        request,
                        f"Le lien d'activation est invalide ou a expiré. <a href='{resend_link}'>Renvoyer un lien</a>"
                    )
                    return redirect('app:home')
                user = authenticate(request, username=user.username, password=pwd)
                print("user authenticated")
                if user is not None:
                    django_login(request, user)
                    messages.success(request, "Connexion réussie.")
                    print('connected')
                    return redirect('app:home')
                else:
                    print("wrong password")
                    messages.error(request, "Email ou mot de passe incorrect.")
            except User.DoesNotExist:
                print("user not found")
                messages.error(request, "Aucun utilisateur trouvé avec cet email.")
    
    return render(request, 'applicompte/login.html')

def logout(request): 
    django_logout(request)
    messages.success(request, "Déconnexion réussie.")
    return render(
        request,
        'applicompte/logout.html'
    )

def forgetpassword(request):
    if request.user.is_authenticated:
        messages.info(request, "Vous êtes déjà connecté. Déconnectez-vous pour utiliser cette fonctionnalité.")
        return redirect('applicompte:editpassword')  # Redirige vers une vue où l'utilisateur connecté peut changer son mot de passe

    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.error(request, "Veuillez entrer une adresse email.")
            return render(request, 'applicompte/forgetpassword.html')

        try:
            user = User.objects.get(email=email)
            # Génération du lien sécurisé
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{request.scheme}://{request.get_host()}{reverse('applicompte:reset_password', kwargs={'uidb64': uid, 'token': token})}"

            # Envoi de l'email
            subject = "Réinitialisation de votre mot de passe"
            message = f"Bonjour {user.username},\n\nCliquez sur le lien suivant pour réinitialiser votre mot de passe :\n{reset_link}\n\nSi vous n'avez pas demandé cette action, veuillez ignorer cet email."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            messages.success(request, "Un email de réinitialisation vous a été envoyé.")
            return redirect('applicompte:login')
        except User.DoesNotExist:
            messages.error(request, "Aucun compte trouvé avec cet email.")
            return render(request, 'applicompte/forgetpassword.html')

    return render(request, 'applicompte/forgetpassword.html')


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password != confirm_password:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return render(request, 'applicompte/reset_password.html')
            
            user.set_password(new_password)
            user.save()
            messages.success(request, "Votre mot de passe a été réinitialisé avec succès.")
            return redirect('applicompte:login')

        return render(request, 'applicompte/reset_password.html', {'valid_link': True})
    else:
        messages.error(request, "Le lien de réinitialisation est invalide ou a expiré.")
        return render(request, 'applicompte/reset_password.html', {'valid_link': False})

def register(request):
    if request.user.is_authenticated:
        return redirect('app:home')
    if request.method == 'POST':
        form = UserCreationSW(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, "Cet email est déjà utilisé.")
                return render(request, 'applicompte/register.html', {'form': form})
            
            user = form.save(commit=False)
            user.username = str(uuid.uuid4())[:30]  # Génère un nom d'utilisateur unique
            user.is_active = False  # Désactiver le compte jusqu'à la validation de l'email
            user.save()
            
            # Génération du lien de validation
            current_site = get_current_site(request)
            mail_subject = 'Activez votre compte'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f"{request.scheme}://{current_site.domain}{reverse('applicompte:activate', kwargs={'uidb64': uid, 'token': token})}"
            
            message = render_to_string('applicompte/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
            
            messages.success(request, "Un email de validation vous a été envoyé. Veuillez vérifier votre boîte de réception.")
            return redirect('app:home')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UserCreationSW()
    return render(request, 'applicompte/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        django_login(request, user)
        messages.success(request, "Votre compte a été activé avec succès.")
        return redirect('app:home')
    else:
        # Lien pour renvoyer l'activation
        resend_link = reverse('applicompte:resend_activation_link', args=[user.id])
        messages.error(
            request,
            f"Le lien d'activation est invalide ou a expiré. <a href='{resend_link}'>Renvoyer un lien</a>"
        )
        return redirect('applicompte:register')

def resend_activation_link(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        if not user.is_active:
            # Générer un nouveau lien d'activation
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f"{request.scheme}://{current_site.domain}/activate/{uid}/{token}/"
            
            # Envoyer un email
            subject = "Renvoyer le lien d'activation"
            message = f"Cliquez sur le lien suivant pour activer votre compte :\n\n{activation_link}"
            send_mail(subject, message, 'noreply@example.com', [user.email])
            
            messages.success(request, "Un nouveau lien d'activation vous a été envoyé.")
        else:
            messages.info(request, "Votre compte est déjà activé.")
    except User.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
    
    return redirect('applicompte:register')


def profile(request):
    if request.user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        return render(request, 'applicompte/profile.html', {'profile': profile})
    else:
        return redirect('login')
    
    
def edit_profile(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)

        # Déterminez quel formulaire utiliser en fonction du type d'utilisateur
        if profile.type_user == 0:  # Standard
            form_class = StandardUserProfileForm
        elif profile.type_user == 1:  # Premium
            form_class = PremiumUserProfileForm
        elif profile.type_user == 2:  # Admin
            form_class = AdminUserProfileForm
        else:
            form_class = StandardUserProfileForm

        if request.method == 'POST':
            form = form_class(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('applicompte:profile')
        else:
            form = form_class(instance=profile)

        return render(request, 'applicompte/edit_profile.html', {'form': form})
    else:
        return redirect('login')
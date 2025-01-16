import os
from django.core.wsgi import get_wsgi_application

# Définit le fichier de configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShareWheel.settings')

# Application WSGI
application = get_wsgi_application()


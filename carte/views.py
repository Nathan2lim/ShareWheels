from django.shortcuts import render
from .models import Lieu

def festival_map(request):
    # Récupération de tous les lieux du festival
    lieux = Lieu.objects.all()
    context = {
        'lieux': lieux,
        # Vous pouvez aussi transmettre d’autres paramètres (par exemple une clé API)
        'MAPBOX_ACCESS_TOKEN': 'sk.eyJ1IjoibmF0aGFuMmxpbSIsImEiOiJjbTk5dDFxMXIwOHI2MmlzNzBvNThpMzA5In0.VIxdNPTpP9geFsScMiVvZg',  
    }
    return render(request, 'carte/carte.html', context)
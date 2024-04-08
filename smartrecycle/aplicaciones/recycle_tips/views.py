from django.shortcuts import render
from .models import Tip

def tips(request):
    mis_tips = Tip.objects.filter(publish=True) # Solo obtiene los objetos Tip con publish = True
    return render(request,"tips.html",{"tips":mis_tips})
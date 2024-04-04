from django.shortcuts import render
from .models import Tip

def tips(request):
    mis_tips = Tip.objects.all()
    return render(request,"tips.html",{"tips":mis_tips})
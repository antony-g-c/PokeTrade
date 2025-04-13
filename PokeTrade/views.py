from django.shortcuts import render
from .models import Card

# home view
def home(request):
    return render(request, "home.html")
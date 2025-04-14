from django.shortcuts import render, redirect
from .models import Card

# home view
def home(request):
    return render(request, "home.html")
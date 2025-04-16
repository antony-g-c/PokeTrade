from django.shortcuts import render, redirect
from .models import Card


def collection(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cards = Card.objects.filter(owner=request.user)

    context = {
        'cards': cards,
        'card_count': cards.count(),
    }

    return render(request, "collection.html", context)
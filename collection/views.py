from django.shortcuts import render, redirect
from .models import Card
from django.contrib.auth.decorators import login_required


def collection(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cards = Card.objects.filter(owner=request.user)

    context = {
        'cards': cards,
        'card_count': cards.count(),
    }

    return render(request, "collection.html", context)

@login_required
def shop(request):
    return render(request, "shop.html")
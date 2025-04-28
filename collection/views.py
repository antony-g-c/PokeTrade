from django.shortcuts import render, redirect
from .models import Card

def collection(request):
    if not request.user.is_authenticated:
        return redirect("login:login")  # corrected to namespaced login if needed

    cards = Card.objects.filter(owner=request.user)

    # Check if user searched for something
    query = request.GET.get('q')
    if query:
        cards = cards.filter(name__icontains=query)

    context = {
        'cards': cards,
        'card_count': cards.count(),
    }

    return render(request, "collection.html", context)
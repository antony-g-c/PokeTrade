from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  
from .models import listing_for_trading, offer_trade
from marketplace1.models import Card
# Create your views here.


def trade(request):
    if request.method=="POST":
        card=get_object_or_404(Card, id=request.POST("card_id"))
        listing_for_trading.objects.create(card=card, owner=request.user)
        messages.success(request, "card posted")
        return redirect("trade:trade")
    return render(request, "trade/trade.html", {"cards": Card.objects.all()})


def offer(request, id):
    listing = get_object_or_404(listing_for_trading, pk = id, open=True)
    card_offered= get_object_or_404(Card, pk = request.POST["card_offered"], card_owner=request.user)
    if listing.card_owner == request.user:
        messages.error(request, "Cannot offer own listing")
    else:
        offer_trade.objects.create(listing=listing, offerer=request.user, card_offered=card_offered)
        messages.success(request, "Offer sent")
    return redirect("trade:listing")

def listing(request):
    open = listing_for_trading.objects.filter(open=True)
    return render(request, "trade/listing.html", {"open": open})


def offer_management(request):
    listings = listing_for_trading.objects.filter(owner=request.user)
    return render(request, "trade/offer_management.html", {"listings": listings})

def offer_response(request, id):
    offer = get_object_or_404(offer_trade, pk=id)
    act = request.POST["action"]
    if offer.listing.owner != request.user:
        messages.error(request, "Cannot respond to own offer")
    else:
        if act =="accept":
            list = offer.listing_for_trading
            x, y = list.card, offer.card_offered
            owner1, owner2 = list.card_owner, offer.card_offered_by
            x.card_owner, y.card_owner = owner2, owner1
            x.save()
            y.save()
            list.open=False
            list.save()
            offer.choice="accepted"
            messages.success(request, "Offer accepted")
        else:
            offer.choice="rejected"
            messages.success(request, "Offer rejected")
        offer.save()
    return redirect("trade:offer_management")

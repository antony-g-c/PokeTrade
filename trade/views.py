from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  
from .models import OfferTrade, ListingForTrading
from marketplace1.models import Card

def trade(request):
    if request.method == "POST":
        card = get_object_or_404(Card, id=request.POST.get("card_id"))
        ListingForTrading.objects.create(card=card, owner=request.user)
        messages.success(request, "Card posted for trade.")
        return redirect("trade:trade")
    return render(request, "trade/trade.html", {"cards": Card.objects.all()})

def offer(request, id):
    listing = get_object_or_404(ListingForTrading, pk=id, is_open=True)
    card_offered = get_object_or_404(Card, pk=request.POST.get("card_offered"), owner=request.user)
    if listing.owner == request.user:
        messages.error(request, "Cannot offer on your own listing.")
    else:
        OfferTrade.objects.create(listing=listing, offered_by=request.user, card_offered=card_offered)
        messages.success(request, "Offer sent.")
    return redirect("trade:listing")

def listing(request):
    listings = ListingForTrading.objects.filter(is_open=True)
    return render(request, "trade/listing.html", {"listings": listings})

def offer_management(request):
    listings = ListingForTrading.objects.filter(owner=request.user)
    return render(request, "trade/offer_management.html", {"listings": listings})

def offer_response(request, id):
    offer = get_object_or_404(OfferTrade, pk=id)
    act = request.POST.get("action")
    if offer.listing.owner != request.user:
        messages.error(request, "Cannot respond to offers on listings not owned by you.")
    else:
        if act == "accept":
            listing = offer.listing
            x, y = listing.card, offer.card_offered
            owner1, owner2 = listing.owner, offer.offered_by
            x.owner, y.owner = owner2, owner1
            x.save()
            y.save()
            listing.is_open = False
            listing.save()
            offer.choice = "ACCEPTED"
            messages.success(request, "Offer accepted.")
        else:
            offer.choice = "REJECTED"
            messages.success(request, "Offer rejected.")
        offer.save()
    return redirect("trade:offer_management")

def create_listing(request):
    if request.method == "POST":
        card_id = request.POST.get("card_id")
        card = get_object_or_404(Card, id=card_id, owner=request.user)
        ListingForTrading.objects.create(card=card, owner=request.user)
        messages.success(request, "Card listed for trade.")
        return redirect("trade:listing")
    cards = Card.objects.filter(owner=request.user)
    return render(request, "trade/create_listing.html", {"cards": cards})
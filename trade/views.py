from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  
from .models import OfferTrade, ListingForTrading
from marketplace1.models import Card
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def trade(request):
    if request.method == "POST":
        card = get_object_or_404(Card, id=request.POST.get("card_id"))
        ListingForTrading.objects.create(card=card, owner=request.user)
        messages.success(request, "Card posted for trade.")
        return redirect("trade:trade")
    return render(request, "trade/trade.html", {"cards": Card.objects.all()})

@require_http_methods(["GET", "POST"])
@login_required
def offer(request, id):
    listing = get_object_or_404(ListingForTrading, pk=id, is_open=True)

    if request.method == "POST":
        card_offered_id = request.POST.get("card_offered")
        card_offered = get_object_or_404(Card, pk=card_offered_id, owner=request.user)

        if listing.owner == request.user:
            messages.error(request, "Cannot offer on your own listing.")
        else:
            OfferTrade.objects.create(listing=listing, offered_by=request.user, offered_card=card_offered)
            messages.success(request, f"You offered {card_offered.name} for {listing.listed_card.name}.")
        return redirect("trade:sent_offers")

    # If GET request, show a form to choose which card to offer
    user_cards = Card.objects.filter(owner=request.user)
    return render(request, "trade/make_offer.html", {"listing": listing, "user_cards": user_cards})
def listing(request):
    query = request.GET.get('q')
    listings = ListingForTrading.objects.filter(is_open=True)

    if query:
        listings = listings.filter(
            Q(listed_card__name__icontains=query) |
            Q(listed_card__pokemon__icontains=query)
        )

    return render(request, "trade/listing.html", {"listings": listings})

@login_required
def offer_management(request):
    listings = ListingForTrading.objects.filter(owner=request.user)
    return render(request, "trade/offer_management.html", {"listings": listings})
@login_required
def offer_response(request, id):
    offer = get_object_or_404(OfferTrade, pk=id)
    act = request.POST.get("action")
    if offer.listing.owner != request.user:
        messages.error(request, "Cannot respond to offers on listings not owned by you.")
    else:
        if act == "accept":
            listing = offer.listing
            x, y = listing.listed_card, offer.offered_card
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
@login_required
def create_listing(request):
    if request.method == "POST":
        card_id = request.POST.get("card_id")
        card = get_object_or_404(Card, id=card_id, owner=request.user)
        ListingForTrading.objects.create(listed_card=card, owner=request.user)
        messages.success(request, "Card listed for trade.")
        return redirect("trade:listing")
    cards = Card.objects.filter(owner=request.user)
    return render(request, "trade/create_listing.html", {"cards": cards})

@login_required
def trade_listing_delete(request, pk):
    listing = get_object_or_404(ListingForTrading, pk=pk, owner=request.user, is_open=True)

    if request.method == "POST":
        listing.delete()
        messages.success(request, "Trade listing deleted successfully.")
        return redirect("trade:offer_management")

    return render(request, "trade/confirm_delete.html", {"listing": listing})
@login_required
def sent_offers(request):
    offers = OfferTrade.objects.filter(offered_by=request.user)
    return render(request, 'trade/sent_offers.html', {'sent_offers': offers})

@require_POST
@login_required
def rescind_offer(request, id):
    offer = get_object_or_404(OfferTrade, pk=id, offered_by=request.user, choice='PENDING')
    offer.delete()
    messages.success(request, "Your offer has been rescinded.")
    return redirect('trade:sent_offers')
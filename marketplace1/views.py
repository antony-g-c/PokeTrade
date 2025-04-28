from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .forms import ListingForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import requests


from .models import Card

def poke_card(request):
    cards = Card.objects.all()
    return render(request, 'poke_card.html', {'cards': cards})


def details(request, id):
    myCard = get_object_or_404(Card, id=id)

    extra_info = {}

    # Only if card has a valid image URL
    if myCard.image:
        # Example: https://images.pokemontcg.io/xy5/48.png
        try:
            parts = myCard.image.split('/')
            set_id = parts[-2]  # e.g., 'xy5'
            card_number = parts[-1].replace('.png', '')  # e.g., '48'
            tcg_id = f"{set_id}-{card_number}"  # e.g., 'xy5-48'

            url = f"https://api.pokemontcg.io/v2/cards/{tcg_id}"
            headers = {"X-Api-Key": "YOUR-API-KEY"}  # Replace or remove if not needed
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json().get('data', {})
                extra_info = {
                    'name': data.get('name'),
                    'set': data.get('set', {}).get('name'),
                    'rarity': data.get('rarity'),
                    'subtypes': data.get('subtypes', []),
                    'number': data.get('number'),
                    'prices': data.get('tcgplayer', {}).get('prices', {}),
                }
        except Exception as e:
            print("Error fetching TCG info:", e)

    return render(request, 'details.html', {'myCard': myCard, 'extra_info': extra_info})
@login_required
def listing_create(request):
    if request.method == "POST":
        form = ListingForm(request.POST, user=request.user)
        if form.is_valid():
            listing = form.save(commit=False)
            if listing.card.owner != request.user:
                form.add_error("card", "You can only list cards you own.")
            else:
                listing.seller = request.user
                listing.is_active = True
                listing.save()
                messages.success(request, "Your card is now listed for sale!")
                return redirect("marketplace1:marketplace")
    else:
        form = ListingForm(user=request.user)

    return render(request, "marketplace1/listing_form.html", {"form": form})

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, "listing_detail.html", {"listing": listing})

@login_required
def listing_buy(request, pk):
    listing = get_object_or_404(Listing, pk=pk, is_active=True)
    if listing.seller == request.user:
        messages.error(request, "You can’t buy your own listing.")
    else:
        # transfer ownership
        card = listing.card
        card.owner = request.user
        card.save()

        # record an Order
        Order.objects.create(
            user=request.user,
            purchased_card=card,
            seller=listing.seller,
            total=listing.price,
            quantity=1
        )

        listing.is_active = False
        listing.save()
        messages.success(request, f"You bought {card.name} for ${listing.price}!")
    return redirect("marketplace1:marketplace")

from orders.models import Order
from marketplace1.models import Listing  # Just making sure you imported

@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user, is_active=True)

    if request.method == "POST":
        listing.delete()
        messages.success(request, "Listing deleted successfully.")
        return redirect("marketplace1:marketplace")

    return render(request, "marketplace1/confirm_delete.html", {"listing": listing})


def marketplace(request):
    query = request.GET.get('q', '')  # Get search query from URL

    listings = Listing.objects.filter(is_active=True).select_related('card', 'seller')

    orders = None
    my_listings = None
    if query:
        listings = listings.filter(
            Q(card__name__icontains=query) |
            Q(card__pokemon__icontains=query)
        )
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-date')
        my_listings = Listing.objects.filter(seller=request.user, is_active=True)

    return render(request, 'marketplace.html', {
        'listings': listings,
        'orders': orders,
        'my_listings': my_listings,
        'query': query,
    })
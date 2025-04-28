from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Card, Listing
from django.template import loader
from django.contrib import messages
from .forms import ListingForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from orders.models import Order
from marketplace1.models import Listing

def poke_card(request):
    myCard = Card.objects.all().values()
    template = loader.get_template('poke_card.html')
    context = {
        'myCard': myCard,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    myCard = Card.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'myCard': myCard,
    }
    return HttpResponse(template.render(context, request))

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

from django.contrib.auth.decorators import login_required


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
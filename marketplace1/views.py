from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Card, Listing
from django.template import loader
from django.contrib import messages
from django.contrib.auth.models import User



from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts           import get_object_or_404, redirect, render
from .forms  import ListingForm
from .models import Listing
# Create your views here.

def poke_card(request):
    myCard = Card.objects.all().values()
    template = loader.get_template('poke_card.html')
    context = {
        'myCard': myCard,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    myCard = Card.objects.get(id=id).get(id=id)
    template = loader.get_template('details.html')
    context = {
        'myCard': myCard,
    }
    return HttpResponse(template.render(context, request))



@login_required
def listing_create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            # guard: only list your own cards
            if listing.card.owner != request.user:
                form.add_error("card", "You can only list cards you own.")
            else:
                listing.seller = request.user
                listing.save()
                messages.success(request, "Your card is now listed for sale!")
                return redirect("marketplace1:listing_list")
    else:
        form = ListingForm()
    return render(request, "marketplace1/listing_form.html", {"form": form})


def listing_list(request):
    qs = Listing.objects.filter(is_active=True).select_related("card", "seller")
    return render(request, "marketplace1/listing_list.html", {"listings": qs})


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, "marketplace1/listing_detail.html", {"listing": listing})


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
        listing.is_active = False
        listing.save()
        messages.success(request, f"You bought {card.name} for ${listing.price}!")
    return redirect("marketplace1:listing_list")

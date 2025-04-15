from django.shortcuts import render
from django.http import HttpResponse
from .models import Card
from django.template import loader



# Create your views here.

def poke_card(request):
    myCard = Card.objects.all().values()
    template=loader.get_template('poke_card.html')
    context = {
        'myCard': myCard,
    }
    return HttpResponse(template.render(context,request))


def details(request, id):
    myCard = Card.objects.get(id=id)
    template=loader.get_template('details.html')
    context = {
        'myCard': myCard,
    }
    return HttpResponse(template.render(context,request))
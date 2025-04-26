import requests
import random
from collection.models import Card
from django.conf import settings

POKEAPI = "https://pokeapi.co/api/v2/pokemon/%d"


APITCG = "https://apitcg.com/api/pokemon/cards?name=%s"

def generatePokemon(num, user):
    cards = []
    for _ in range(num):
        cards.append(addRandomPokemon(user))
    return cards

headers = {
    "x-api-key": settings.TCG_API_KEY,
}

def addRandomPokemon(user):
    while True:
        pokemon = requests.get(POKEAPI % random.randint(1, 1025)).json()["name"]
        cards = requests.get(APITCG % pokemon, headers=headers).json()
        if cards["totalCount"] > 0:
            break
    card = cards["data"][random.randint(0, cards["totalCount"] - 1)]
    created = Card.objects.create(
        owner = user,
        name = card["name"],
        pokemon = pokemon,
        price = card["cardmarket"]["prices"]["averageSellPrice"],
        image = card["images"]["small"],
    )
    return created
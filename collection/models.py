from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

#Model for a Pokemon card
class Card(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    pokemon = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    image = models.CharField(max_length=200)
    
    def __str__(self):
        return self.pokemon
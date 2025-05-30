from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

def get_admin_user():
    try:
        return User.objects.get(username='admin').id
    except User.DoesNotExist:
        return None
#Model for a Pokemon card
class Card(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,  default=get_admin_user())
    name = models.CharField(max_length=50)
    pokemon = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.CharField(max_length=200)
    
    def __str__(self):
        return self.pokemon
from django.db import models
from django.contrib.auth.models import User
from collection.models import Card
from django.conf import settings

def get_admin_user():
    try:
        return User.objects.get(username='admin').id
    except User.DoesNotExist:
        return None

class Listing(models.Model):
    card       = models.ForeignKey(Card,
                                   on_delete=models.CASCADE,
                                   related_name="listings")
    seller     = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
                                   related_name="listings")
    price      = models.DecimalField(max_digits=8, decimal_places=2)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card.name} for ${self.price} by {self.seller.username}"




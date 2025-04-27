from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

def get_admin_user():
    try:
        return User.objects.get(username='admin').id
    except User.DoesNotExist:
        return None
# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField() 
    type = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards',  default=get_admin_user())  # Added owner field


    def __str__(self):
        return self.name


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




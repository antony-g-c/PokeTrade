from django.db import models
from django.db.models import ForeignKey

# Create your models here.

class listing_for_trading(models.Model):
    card = ForeignKey('Card', on_delete=models.CASCADE, related_name='listings')
    card_owner = ForeignKey('User', on_delete=models.CASCADE, related_name='listings')
    open = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)

class offer_trade(models.Model):
    listing = ForeignKey('listing_for-trading', on_delete=models.CASCADE, related_name='offers')
    trade_offered_by = ForeignKey('User', on_delete=models.CASCADE, related_name='offers')
    card_offered = ForeignKey('Card', on_delete=models.CASCADE, related_name='offers')
    choice  = models.CharField(max_length=10,choices=[("PENDING","Pending"),("ACCEPTED","Accepted"),("REJECTED","Rejected")],default="PENDING")
    date = models.DateTimeField(auto_now_add=True)




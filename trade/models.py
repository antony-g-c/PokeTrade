from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

def get_admin_user():
    try:
        return User.objects.get(username='admin').id
    except User.DoesNotExist:
        return None

class ListingForTrading(models.Model):
    card = models.ForeignKey('marketplace1.Card', on_delete=models.CASCADE, related_name='trade_listings')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_listings', default=get_admin_user())
    is_open = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trading listing for {self.card.name} by {self.owner.username}"

    class Meta:
        ordering = ["-date"]

class OfferTrade(models.Model):
    listing = models.ForeignKey(ListingForTrading, on_delete=models.CASCADE, related_name='offers')
    offered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_offers')
    card_offered = models.ForeignKey('marketplace1.Card', on_delete=models.CASCADE, related_name='trade_offers')
    CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected")
    ]
    choice = models.CharField(max_length=10, choices=CHOICES, default="PENDING")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer by {self.offered_by.username} on {self.listing.card.name} ({self.choice})"

    class Meta:
        ordering = ["-date"]




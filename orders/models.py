from django.conf import settings
from django.db import models

class Order(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    purchased_card      = models.ForeignKey('collection.Card', on_delete=models.CASCADE)
    seller    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales')
    total     = models.DecimalField(max_digits=8, decimal_places=2)
    quantity  = models.PositiveIntegerField(default=1)
    date      = models.DateTimeField(auto_now_add=True)
    status    = models.CharField(max_length=20, default='Completed')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
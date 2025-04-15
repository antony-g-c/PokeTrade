from django.db import models

# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    image = models.URLField() 
    type = models.CharField(max_length=250)
    price = models.DecimalField(max_digits = 20, decimal_places = 2)

from django import forms
from .models import Card, Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model  = Listing
        fields = ["card", "price"]
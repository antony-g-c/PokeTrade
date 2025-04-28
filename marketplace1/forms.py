from django import forms
from .models import Listing, Card

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['card', 'price']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Extract 'user' from kwargs
        super().__init__(*args, **kwargs)
        self.fields['card'].queryset = Card.objects.filter(owner=user)
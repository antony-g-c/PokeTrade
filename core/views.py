from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse  
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from core.forms import UserCreationForm
from django.contrib.auth.models import User
"""
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token   
from django.core.mail import EmailMessage
"""

# Create your views here.
def home(request):
    count= User.objects.count()
    return render(request, 'home.html',{'count':count})

def signup(request):
    if request.method == 'POST':  
        form = UserCreationForm(request.POST)  
        if form.is_valid():  
            user=form.save()
            login(request, user)
            return redirect('movieStore:movies')
    else:  
        form = UserCreationForm()    
    return render(request, 'registration/signup.html', {'form':form})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.cart_orders.all()
    return render(request, 'orders.html',
        {'template_data': template_data})

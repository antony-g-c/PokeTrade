from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='login'),
    path('signup/', views.signup, name='signup'),
    path('', include('django.contrib.auth.urls')),
]
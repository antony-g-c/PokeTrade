from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.collection, name='collection'),
    path('shop/', views.shop, name='shop')
]
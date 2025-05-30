from django.urls import path
from . import views

app_name = 'marketplace1'  # important for {% url 'marketplace1:listing_create' %} to work

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('cards/', views.poke_card, name='poke_card'),  # removed 'marketplace1/'
    path('details/<int:id>/', views.details, name='details'),
    path('list/new/', views.listing_create, name='listing_create'),
    path('list/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('list/<int:pk>/buy/', views.listing_buy, name='listing_buy'),
    path('list/<int:pk>/delete/', views.listing_delete, name='listing_delete'),
]
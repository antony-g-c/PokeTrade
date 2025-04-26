from django.urls import path

from . import views

urlpatterns=[
    path('marketplace1/', views.poke_card, name='poke_card'),
    path('marketplace1/details/<int:id>', views.details, name='details'),
    path("list/",              views.listing_list,    name="listing_list"),
    path("list/new/",          views.listing_create,  name="listing_create"),
    path("list/<int:pk>/",     views.listing_detail,  name="listing_detail"),
    path("list/<int:pk>/buy/", views.listing_buy,     name="listing_buy"),
]
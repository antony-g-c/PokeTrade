from django.urls import path

from . import views

urlpatterns=[
    path('marketplace1/', views.poke_card, name='poke_card'),
    path('marketplace1/details/<int:id>', views.details, name='details'),
]
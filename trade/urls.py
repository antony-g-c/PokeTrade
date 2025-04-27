from django.urls import path

from . import views

urlpatterns=[
    path("create/", views.create_listing, name="create_listing"),
    path("", views.listing, name="listing"),
    path("details/<int:id>", views.details, name="details"),
    path("manage/", views.manage_cards, name="manage_cards"),
    path("offer/<int:id>", views.offer, name="offer"),
    path("response/<int:id>", views.offer_response, name="offer_response"),
    path("trade/", views.trade, name="trade"),
    path("offer_management/", views.offer_management, name="offer_management"),
]

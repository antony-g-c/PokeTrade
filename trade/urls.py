from django.urls import path
from . import views

app_name = 'trade'

urlpatterns = [
    path("create/", views.create_listing, name="create_listing"),
    path("", views.listing, name="listing"),
    path("offer/<int:id>", views.offer, name="offer"),
    path("response/<int:id>", views.offer_response, name="offer_response"),
    path("", views.trade, name="trade"),
    path("offer_management/", views.offer_management, name="offer_management"),
    path("sent_offers/", views.sent_offers, name="sent_offers"),
    path('rescind_offer/<int:id>/', views.rescind_offer, name='rescind_offer'),
]
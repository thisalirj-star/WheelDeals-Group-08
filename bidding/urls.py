from django.urls import path
from . import views

urlpatterns = [
    path('', views.bidding_page, name='bidding'),

    path('buyer/<int:car_id>/', views.buyer_bidding_page, name='buyer_bidding_page'),
    path('seller/<int:car_id>/', views.seller_bidding_page, name='seller_bidding_page'),

    path('place-bid/<int:car_id>/', views.place_bid, name='place_bid'),
    path('delete-bid/<int:bid_id>/', views.delete_bid, name='delete_bid'),

    path('remove-bid/<int:bid_id>/', views.remove_bid_seller, name='remove_bid_seller'),
    path('accept-bid/<int:car_id>/', views.accept_highest_bid, name='accept_highest_bid'),
    path('extend-time/<int:car_id>/', views.extend_bidding_time, name='extend_bidding_time'),
]
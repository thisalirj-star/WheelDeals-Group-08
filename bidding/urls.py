from django.urls import path
from . import views

urlpatterns = [
    # Main bidding page (temporary - will remove later)
    path('', views.bidding_page, name='bidding'),
    
    # Buyer views
    path('buyer/<int:car_id>/', views.buyer_bidding_page, name='buyer_bidding_page'),
    path('buyer/place/<int:car_id>/', views.place_bid, name='place_bid'),
    path('buyer/delete/<int:bid_id>/', views.delete_bid, name='delete_bid'),
    
    # Seller views
    path('seller/<int:id>/', views.seller_bidding_page, name='seller_bidding_page'),
    path('seller/remove/<int:bid_id>/', views.remove_bid_seller, name='remove_bid_seller'),
    path('seller/accept/<int:car_id>/', views.accept_highest_bid, name='accept_highest_bid'),
    path('seller/extend/<int:car_id>/', views.extend_bidding_time, name='extend_bidding_time'),
]
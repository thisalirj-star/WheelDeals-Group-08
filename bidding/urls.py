from django.urls import path
from . import views

urlpatterns = [

    # Buyer
    path('buyer/<int:auction_id>/',         views.buyer_bidding_page, name='buyer_bidding_page'),
    path('buyer/place/<int:auction_id>/',   views.place_bid,          name='place_bid'),
    path('buyer/delete/<int:bid_id>/',      views.delete_bid,         name='delete_bid'),

    # Seller
    path('seller/<int:id>/',                views.seller_bidding_page,  name='seller_bidding_page'),
    path('seller/pause/<int:id>/',          views.pause_auction,        name='pause_auction'),
    path('seller/resume/<int:id>/',         views.resume_auction,       name='resume_auction'),
    path('seller/remove/<int:bid_id>/',     views.remove_bid_seller,    name='remove_bid_seller'),
    path('seller/accept/<int:id>/',         views.accept_highest_bid,   name='accept_highest_bid'),
    path('seller/extend/<int:id>/',         views.extend_bidding_time,  name='extend_bidding_time'),
    path('seller/delete/<int:id>/',         views.delete_auction,       name='delete_auction'),  # NEW

]
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Bid 


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Bid


# MAIN PAGE
def bidding_page(request):
    bids = Bid.objects.all()
    return render(request, 'bidding/bidding.html', {'bids': bids})


# BUYER VIEW
def buyer_bidding_page(request, car_id):
    bids = Bid.objects.filter(car_id=car_id)

    return render(request, 'bidding/buyer_bidding.html', {
        'bids': bids,
        'car_id': car_id
    })


# SELLER VIEW
def seller_bidding_page(request, car_id):
    bids = Bid.objects.filter(car_id=car_id)

    return render(request, 'bidding/seller_bidding.html', {
        'bids': bids,
        'car_id': car_id
    })


# PLACE BID
def place_bid(request, car_id):
    if request.method == "POST":
        amount = request.POST.get('bid_amount')

        Bid.objects.create(
            user=User.objects.first(),  # temp user
            amount=amount,
            car_id=car_id
        )

    return redirect('buyer_bidding_page', car_id=car_id)


# DELETE OWN BID
def delete_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    bid.delete()
    return redirect('bidding')


# SELLER REMOVE BID
def remove_bid_seller(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    car_id = bid.car_id
    bid.delete()
    return redirect('seller_bidding_page', car_id=car_id)


# ACCEPT HIGHEST BID
def accept_highest_bid(request, car_id):
    highest = Bid.objects.filter(car_id=car_id).order_by('-amount').first()

    if highest:
        Bid.objects.filter(car_id=car_id).exclude(id=highest.id).delete()

    return redirect('seller_bidding_page', car_id=car_id)


# EXTEND TIME (dummy)
def extend_bidding_time(request, car_id):
    return redirect('seller_bidding_page', car_id=car_id)
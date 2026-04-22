from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import Bid

# MAIN PAGE (will remove later when connecting)
def bidding_page(request):
    bids = Bid.objects.all()
    return render(request, 'bidding/bidding.html', {'bids': bids})

# BUYER VIEW
def buyer_bidding_page(request, car_id):
    bids = Bid.objects.filter(car_id=car_id)
    
    # Dummy car data until Sithmi's car app is ready
    car = {
        'id': car_id,
        'title': 'Toyota Prius 2018',
        'starting_price': 4500000,
        'mileage': 50000,
        'location': 'Colombo'
    }
    
    auction_end = timezone.now() + timedelta(hours=2)

    return render(request, 'bidding/buyer_bidding.html', {
       'bids': bids,
       'car': car,
       'car_id': car_id,
       'auction_end': auction_end,
       
    })

# SELLER VIEW
from .models import Auction

def seller_bidding_page(request, id):
    auction = Auction.objects.get(id=id)
    bids = Bid.objects.all()  # or filter properly later

    return render(request, 'bidding/seller_bidding.html', {
        'auction': auction,
        'bids': bids,
    })


# PLACE BID
def place_bid(request, car_id):
    if request.method == "POST":
        amount = request.POST.get('bid_amount')
        
        # Check if amount is valid
        if amount and int(amount) > 0:
            # Get logged-in user, or create a test user for now
            if request.user.is_authenticated:
                user = request.user
            else:
                # Temporary: get or create a test user
                user, created = User.objects.get_or_create(
                    username='test_buyer',
                    defaults={'email': 'test@example.com'}
                )
            
            Bid.objects.create(
                user=user,
                amount=amount,
                car_id=car_id
            )
    
    return redirect('buyer_bidding_page', car_id=car_id)

# DELETE OWN BID (Buyer)
def delete_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    car_id = bid.car_id
    bid.delete()
    return redirect('buyer_bidding_page', car_id=car_id)

# SELLER REMOVE BID
def remove_bid_seller(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    car_id = bid.car_id
    bid.delete()
    return redirect('seller_bidding_page', car_id=car_id)

# ACCEPT HIGHEST BID (keeps only highest, deletes others)
def accept_highest_bid(request, car_id):
    highest = Bid.objects.filter(car_id=car_id).order_by('-amount').first()
    
    if highest:
        # Keep only the highest bid, delete all others
        Bid.objects.filter(car_id=car_id).exclude(id=highest.id).delete()
    
    return redirect('seller_bidding_page', car_id=car_id)

# EXTEND TIME (updated with actual functionality)
def extend_bidding_time(request, car_id):
    # Get all bids for this car and add 1 hour to their end_time
    # (Assuming your Bid model has an end_time field)
    bids = Bid.objects.filter(car_id=car_id)
    for bid in bids:
        if hasattr(bid, 'end_time') and bid.end_time:
            bid.end_time += timedelta(hours=1)
            bid.save()
    
    return redirect('seller_bidding_page', car_id=car_id)
from django.shortcuts import render, redirect


# Fake database (global for now)
cars_data = [
    {
        "id": 1,
        "name": "Toyota Axio",
        "brand": "Toyota",
        "price": 5000000,
        "status": "Available",
        "views": 120,
        "bid_seconds": 3600  # 1 hour
    },
    {
        "id": 2,
        "name": "Honda Vezel",
        "brand": "Honda",
        "price": 8000000,
        "status": "Sold",
        "views": 340,
        "bid_seconds": 0
    }
]


def seller_dashboard(request):
    context = {
        "cars": cars_data,
        "total_cars_sold": 1,
        "total_revenue": "8,000,000"
    }
    return render(request, "cars/dashboard.html", context)


def car_detail(request, id):
    for car in cars_data:
        if car["id"] == id:
            car["views"] += 1  # 🔥 increase views
            return render(request, "cars/car_detail.html", {"car": car})

    return redirect("dashboard")

    #from django.contrib.auth.decorators import login_required
from bidding.models import Bid, Auction


def buyer_dashboard(request):
    from bidding.models import Bid, Auction

    # Handle anonymous user for preview purposes
    if not request.user.is_authenticated:
        context = {
            'total_bids':    0,
            'winning_count': 0,
            'outbid_count':  0,
            'highest_bid':   None,
            'active_bids':   [],
            'ended_bids':    [],
        }
        return render(request, 'cars/buyer_dashboard.html', context)

    # All bids placed by this buyer
    all_bids = Bid.objects.filter(
        buyer=request.user
    ).select_related('auction', 'auction__car').order_by('-created_at')

    active_bids = [b for b in all_bids if b.auction.status == 'ACTIVE']
    ended_bids  = [b for b in all_bids if b.auction.status == 'ENDED']

    total_bids  = all_bids.count()
    highest_bid = all_bids.order_by('-amount').first()
    highest_bid = highest_bid.amount if highest_bid else None

    winning_count = 0
    outbid_count  = 0
    for bid in active_bids:
        top = bid.auction.bids.first()
        if top and top.buyer == request.user:
            winning_count += 1
        else:
            outbid_count += 1

    context = {
        'total_bids':    total_bids,
        'winning_count': winning_count,
        'outbid_count':  outbid_count,
        'highest_bid':   highest_bid,
        'active_bids':   active_bids,
        'ended_bids':    ended_bids,
    }
    return render(request, 'cars/buyer_dashboard.html', context)
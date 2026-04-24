from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .models import Bid, Auction
from cars.models import Car


# ─────────────────────────────────────────
# BUYER VIEW
# ─────────────────────────────────────────
def buyer_bidding_page(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    bids = auction.bids.all()
    return render(request, 'bidding/buyer_bidding.html', {
        'auction': auction,
        'bids': bids,
        'auction_end': auction.end_time,
    })


# ─────────────────────────────────────────
# PLACE BID (Buyer)
# ─────────────────────────────────────────
@login_required
def place_bid(request, auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auction, id=auction_id)
        amount = request.POST.get('bid_amount')
        if amount and float(amount) > 0:
            highest = auction.bids.first()
            if highest is None or float(amount) > float(highest.amount):
                Bid.objects.create(
                    auction=auction,
                    buyer=request.user,
                    amount=amount,
                )
    return redirect('buyer_bidding_page', auction_id=auction_id)


# ─────────────────────────────────────────
# DELETE OWN BID (Buyer)
# ─────────────────────────────────────────
@login_required
def delete_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id, buyer=request.user)
    auction_id = bid.auction.id
    bid.delete()
    return redirect('buyer_bidding_page', auction_id=auction_id)


# ─────────────────────────────────────────
# SELLER VIEW
# ─────────────────────────────────────────
def seller_bidding_page(request, id):
    auction = get_object_or_404(Auction, id=id)
    bids = auction.bids.order_by('-amount')   # ← must be ordered highest first
    top_bid = bids.first()
    profit = top_bid.amount - auction.car.starting_price if top_bid else 0
    return render(request, 'bidding/seller_bidding.html', {
        'auction': auction,
        'bids': bids,
        'profit': profit,
    })


# ─────────────────────────────────────────
# PAUSE AUCTION (Seller only)
# ─────────────────────────────────────────
@login_required
def pause_auction(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.user != auction.car.seller:
        return redirect('seller_bidding_page', id=id)
    if request.method == "POST" and auction.status == 'ACTIVE':
        auction.status = 'PAUSED'
        auction.save()
    return redirect('seller_bidding_page', id=id)


# ─────────────────────────────────────────
# RESUME AUCTION (Seller only)
# ─────────────────────────────────────────
@login_required
def resume_auction(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.user != auction.car.seller:
        return redirect('seller_bidding_page', id=id)
    if request.method == "POST" and auction.status == 'PAUSED':
        auction.status = 'ACTIVE'
        auction.save()
    return redirect('seller_bidding_page', id=id)


# ─────────────────────────────────────────
# SELLER REMOVE ANY BID
# ─────────────────────────────────────────
@login_required
def remove_bid_seller(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    auction_id = bid.auction.id
    bid.delete()
    return redirect('seller_bidding_page', id=auction_id)


# ─────────────────────────────────────────
# ACCEPT HIGHEST BID (Seller — ends auction)
# ─────────────────────────────────────────
@login_required
def accept_highest_bid(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.user != auction.car.seller:
        return redirect('seller_bidding_page', id=id)
    highest = auction.bids.first()
    if highest:
        auction.bids.exclude(id=highest.id).delete()
        car = auction.car
        car.is_sold = True
        car.sold_to = highest.buyer
        car.sold_price = highest.amount
        car.is_active = False
        car.save(update_fields=['is_sold', 'sold_to', 'sold_price', 'is_active'])
        auction.status = 'ENDED'
        auction.save()
    return redirect('seller_bidding_page', id=id)


# ─────────────────────────────────────────
# EXTEND BIDDING TIME (Seller)
# ─────────────────────────────────────────
@login_required
def extend_bidding_time(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.user != auction.car.seller:
        return redirect('seller_bidding_page', id=id)
    if request.method == "POST":
        hours = int(request.POST.get('extend_hours', 1))
        auction.end_time += timedelta(hours=hours)
        auction.save()
    return redirect('seller_bidding_page', id=id)


# ─────────────────────────────────────────
# DELETE AUCTION (Seller)
# ─────────────────────────────────────────
@login_required
def delete_auction(request, id):
    auction = get_object_or_404(Auction, id=id)
    if request.user != auction.car.seller:
        return redirect('seller_bidding_page', id=id)
    if request.method == "POST":
        auction.delete()
        return redirect('home')
    return redirect('seller_bidding_page', id=id)


# ─────────────────────────────────────────
# CREATE AUCTION (called when seller adds a car)
# ─────────────────────────────────────────
@login_required
def create_auction(request, car_id):
    car = get_object_or_404(Car, id=car_id, seller=request.user)

    # Only create if no active auction exists
    if not car.auctions.filter(status='ACTIVE').exists():
        duration = request.POST.get('duration', '24')
        Auction.objects.create(car=car, duration=duration)

    return redirect('seller_dashboard')

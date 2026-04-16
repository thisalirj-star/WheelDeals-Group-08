from django.shortcuts import render


def buyer_bidding_page(request, car_id):
    return render(request, 'bidding/bidding.html')

def bidding_page(request):
    return render(request, 'bidding/bidding.html')

def place_bid(request, car_id):
    if request.method == "POST":
        amount = request.POST.get('bid_amount')

        # TEMP: avoid crash if user not logged in
        if request.user.is_authenticated:
            Bid.objects.create(
                user=request.user,
                amount=amount
            )

    return redirect('bidding')

def delete_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    # Only allow owner to delete
    if request.user == bid.user:
        bid.delete()

    return redirect('bidding')

def seller_bidding_page(request, car_id):
    bids = Bid.objects.all()

    return render(request, 'bidding/bidding.html', {
        'bids': bids,
        'car_id': car_id
    })

def accept_highest_bid(request, car_id):
    # Get highest bid
    highest_bid = Bid.objects.order_by('-amount').first()

    if highest_bid:
        # For now just delete all other bids (simple logic)
        Bid.objects.exclude(id=highest_bid.id).delete()

    return redirect('bidding')

def remove_bid_seller(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    # Seller removes any bid (no ownership restriction here)
    bid.delete()

    return redirect('bidding')
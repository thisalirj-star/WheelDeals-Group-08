from django.shortcuts import render


def buyer_bidding_page(request, car_id):
    return render(request, 'bidding/bidding.html')

def bidding_page(request):
    return render(request, 'bidding/bidding.html')
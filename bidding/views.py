from django.shortcuts import render


def bidding_page(request):
    return render(request, 'bidding/bidding.html')
# Create your views here.

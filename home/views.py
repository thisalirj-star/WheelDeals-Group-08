from django.shortcuts import render
from django.db.models import Q

def home(request):
    # Get search and filter values from the URL
    search_query = request.GET.get('search', '')
    brand = request.GET.get('brand', '')
    vehicle_type = request.GET.get('vehicle_type', '')
    year = request.GET.get('year', '')
    max_price = request.GET.get('max_price', '')

    # Generate year list for the filter dropdown (2000 to 2025)
    years = list(range(2025, 1999, -1))

    # We will connect to real car data once Amashi sets up the Car model
    # For now we use an empty list so the page loads without errors
    cars = []

    # Summary card data — will be replaced with real database queries later
    total_cars = 0
    active_auctions = 0
    total_sellers = 0
    cars_sold = 0

    context = {
        'cars': cars,
        'search_query': search_query,
        'brand': brand,
        'vehicle_type': vehicle_type,
        'year': year,
        'max_price': max_price,
        'years': years,
        'total_cars': total_cars,
        'active_auctions': active_auctions,
        'total_sellers': total_sellers,
        'cars_sold': cars_sold,
    }

    return render(request, 'home/home.html', context)
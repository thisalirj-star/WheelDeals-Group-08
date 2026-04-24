from django.shortcuts import render
from django.db.models import Q

def home(request):
    search_query = request.GET.get('search', '')
    brand = request.GET.get('brand', '')
    vehicle_type = request.GET.get('vehicle_type', '')
    year = request.GET.get('year', '')
    max_price = request.GET.get('max_price', '')
    years = list(range(2026, 1999, -1))

    try:
        from cars.models import Car
        cars = Car.objects.filter(is_sold=False, is_active=True)

        if search_query:
            cars = cars.filter(
                Q(title__icontains=search_query) |
                Q(brand__icontains=search_query) |
                Q(model__icontains=search_query)
            )
        if brand:
            cars = cars.filter(brand__icontains=brand)
        if vehicle_type:
            cars = cars.filter(vehicle_type=vehicle_type)
        if year:
            cars = cars.filter(year=year)
        if max_price and int(max_price) < 50000000:
            cars = cars.filter(starting_price__lte=max_price)

        cars = cars.order_by('-created_at')

        total_cars      = Car.objects.filter(is_active=True, is_sold=False).count()
        active_auctions = Car.objects.filter(is_active=True, is_sold=False).count()
        total_sellers   = Car.objects.values('seller').distinct().count()
        cars_sold       = Car.objects.filter(is_sold=True).count()

    except Exception:
        cars = []
        total_cars = active_auctions = total_sellers = cars_sold = 0

    context = {
        'cars':           cars,
        'search_query':   search_query,
        'brand':          brand,
        'vehicle_type':   vehicle_type,
        'year':           year,
        'max_price':      max_price,
        'years':          years,
        'total_cars':     total_cars,
        'active_auctions':active_auctions,
        'total_sellers':  total_sellers,
        'cars_sold':      cars_sold,
    }
    return render(request, 'home/home.html', context)
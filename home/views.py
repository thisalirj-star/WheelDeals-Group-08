from django.shortcuts import render

def home(request):
    # Get search and filter values from the URL
    search_query = request.GET.get('search', '')
    brand = request.GET.get('brand', '')
    vehicle_type = request.GET.get('vehicle_type', '')
    year = request.GET.get('year', '')
    max_price = request.GET.get('max_price', '')

    # Generate year list for the filter dropdown
    years = list(range(2026, 1999, -1))

    try:
        # Import Amashi's Car model from the cars app
        from cars.models import Car

        # Start with all active unsold cars
        cars = Car.objects.filter(is_sold=False, is_active=True)

        # Apply search
        if search_query:
            cars = cars.filter(
                title__icontains=search_query
            ) | cars.filter(
                brand__icontains=search_query
            ) | cars.filter(
                model__icontains=search_query
            )

        # Apply filters
        if brand:
            cars = cars.filter(brand__icontains=brand)

        if vehicle_type:
            cars = cars.filter(vehicle_type=vehicle_type)

        if year:
            cars = cars.filter(year=year)

        if max_price and int(max_price) < 50000000:
            cars = cars.filter(starting_price__lte=max_price)

        # Order by newest first
        cars = cars.order_by('-created_at')

        # Summary card data
        total_cars = Car.objects.filter(is_active=True, is_sold=False).count()
        active_auctions = Car.objects.filter(is_active=True, is_sold=False).count()
        total_sellers = Car.objects.values('seller').distinct().count()
        cars_sold = Car.objects.filter(is_sold=True).count()

    except Exception:
        # If cars app is not merged yet, show empty state
        cars = []
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

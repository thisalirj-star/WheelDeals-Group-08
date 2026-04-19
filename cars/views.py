from django.shortcuts import render


def seller_dashboard(request):
    cars = [
        {'id': 1, 'name': 'Toyota Prius', 'brand': 'Toyota', 'price': '6,500,000 LKR'},
        {'id': 2, 'name': 'Honda Civic', 'brand': 'Honda', 'price': '7,200,000 LKR'},
    ]

    context = {
        'total_cars_sold': 2,
        'total_revenue': '13,700,000 LKR',
        'cars': cars
    }
    return render(request, 'cars/dashboard.html', context)


# 🔥 THIS WAS MISSING
def car_detail(request, id):
    car = {
        'id': id,
        'name': 'Sample Car',
        'brand': 'Toyota',
        'price': '5,000,000 LKR'
    }
    return render(request, 'cars/car_detail.html', {'car': car})
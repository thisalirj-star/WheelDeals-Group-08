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
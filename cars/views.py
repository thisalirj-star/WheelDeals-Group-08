from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AddCarForm
from .models import Car
from django.db.models import Avg, Sum
from datetime import datetime


def seller_required(view_func):
    """
    Custom decorator that checks the user is logged in AND is a seller.
    Used instead of @login_required to give a better error message.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_seller():
            messages.error(request, 'Only sellers can access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@seller_required
def add_car_view(request):
    """Add a new car listing. Only accessible by sellers."""
    form = AddCarForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user  # Assign the logged-in seller
            car.save()
            messages.success(request, f'"{car.title}" listed successfully!')
            return redirect('seller_dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'cars/add_car.html', {'form': form})


@seller_required
def edit_car_view(request, car_id):
    """
    Edit an existing car listing.
    get_object_or_404 with seller=request.user ensures
    sellers can only edit THEIR OWN cars.
    """
    car = get_object_or_404(Car, id=car_id, seller=request.user)
    form = AddCarForm(
        request.POST or None,
        request.FILES or None,
        instance=car  # Pre-fills the form with existing data
    )

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'"{car.title}" updated!')
            return redirect('seller_dashboard')

    return render(request, 'cars/add_car.html', {
        'form': form,
        'edit': True,  # Template uses this to change the button label
        'car': car
    })


@seller_required
def delete_car_view(request, car_id):
    """
    Delete a car listing.
    Uses POST confirmation to prevent accidental deletion.
    """
    car = get_object_or_404(Car, id=car_id, seller=request.user)

    if request.method == 'POST':
        title = car.title
        car.delete()
        messages.success(request, f'"{title}" removed.')
        return redirect('seller_dashboard')

    # GET request shows a confirmation page
    return render(request, 'cars/confirm_delete.html', {'car': car})


@seller_required
def seller_dashboard(request):
    """
    Seller dashboard — shows only the logged in seller's cars.
    """
    cars = Car.objects.filter(seller=request.user)
    total_cars = cars.count()
    total_sold = cars.filter(is_sold=False).count()
    sold_count = total_sold
    total_revenue = cars.filter(is_sold=True).aggregate(
        total=Sum('sold_price')
    )['total'] or 0
    avg_price = cars.aggregate(
        avg=Avg('starting_price')
    )['avg'] or 0

        # Most viewed — for now just show latest 3 cars
    most_viewed = [
        {'name': f"{car.brand} {car.model}", 'views': 0}
        for car in cars[:3]
    ]

    # Sales trend — last 6 months
    months = []
    sales_data = []
    for i in range(5, -1, -1):
        from dateutil.relativedelta import relativedelta
        from django.utils import timezone
        month = timezone.now() - relativedelta(months=i)
        month_name = month.strftime('%b')
        month_sales = cars.filter(
            is_sold=True,
            updated_at__year=month.year,
            updated_at__month=month.month
        ).count()
        months.append(month_name)
        sales_data.append(month_sales)

    context = {
        'cars': cars,
        'total_cars': total_cars,
        'total_sold': total_sold,
        'total_revenue': total_revenue,
        'avg_price': avg_price,
        'available_count': available_count,
        'sold_count': sold_count,
        'most_viewed': most_viewed,
        'months': months,
        'sales_data': sales_data,
    }
    return render(request, 'cars/dashboard.html', context)
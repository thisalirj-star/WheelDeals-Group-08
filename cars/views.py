from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AddCarForm
from .models import Car, CarImage
from django.db.models import Avg, Sum
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def seller_required(view_func):
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
    form = AddCarForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user
            car.save()

            # Handle multiple images — max 5
            images = request.FILES.getlist('images')
            for i, img in enumerate(images[:5]):
                CarImage.objects.create(
                    car=car,
                    image=img,
                    is_primary=(i == 0)
                )
                # Also save first image to car.image for backward compatibility
                if i == 0:
                    car.image = img
                    car.save()

            # Auto-create auction if auction_end_time was set
            if car.auction_end_time:
                from bidding.models import Auction
                Auction.objects.create(
                    car=car,
                    end_time=car.auction_end_time,
                    status='ACTIVE'
                )

            messages.success(request, f'"{car.title}" listed successfully!')
            return redirect('seller_dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    return render(request, 'cars/add_car.html', {'form': form})


@seller_required
def edit_car_view(request, car_id):
    car = get_object_or_404(Car, id=car_id, seller=request.user)
    form = AddCarForm(
        request.POST or None,
        request.FILES or None,
        instance=car
    )
    if request.method == 'POST':
        if form.is_valid():
            car = form.save(commit=False)

            # Handle new images if uploaded
            images = request.FILES.getlist('images')
            if images:
                car.images.all().delete()
                for i, img in enumerate(images[:5]):
                    CarImage.objects.create(
                        car=car,
                        image=img,
                        is_primary=(i == 0)
                    )
                    if i == 0:
                        car.image = img

            car.save()

            # Create auction if auction_end_time added and none exists
            if car.auction_end_time:
                from bidding.models import Auction
                if not car.auctions.filter(status='ACTIVE').exists():
                    Auction.objects.create(
                        car=car,
                        end_time=car.auction_end_time,
                        status='ACTIVE'
                    )

            messages.success(request, f'"{car.title}" updated!')
            return redirect('seller_dashboard')

    return render(request, 'cars/add_car.html', {
        'form': form,
        'edit': True,
        'car': car
    })


@seller_required
def delete_car_view(request, car_id):
    car = get_object_or_404(Car, id=car_id, seller=request.user)
    if request.method == 'POST':
        title = car.title
        car.delete()
        messages.success(request, f'"{title}" removed.')
        return redirect('seller_dashboard')
    return render(request, 'cars/confirm_delete.html', {'car': car})


@seller_required
def seller_dashboard(request):
    cars = Car.objects.filter(seller=request.user)

    total_cars = cars.count()
    total_sold = cars.filter(is_sold=True).count()
    available_count = cars.filter(is_sold=False).count()
    sold_count = total_sold
    total_revenue = cars.filter(is_sold=True).aggregate(
        total=Sum('sold_price')
    )['total'] or 0
    avg_price = cars.aggregate(
        avg=Avg('starting_price')
    )['avg'] or 0

    most_viewed = [
        {'name': f"{car.brand} {car.model}", 'views': 0}
        for car in cars[:3]
    ]

    # Sales trend — last 6 months with sample baseline for demo
    months = []
    sales_data = []
    seller_id = request.user.id
    sample_baseline = [
        (seller_id % 3) + 1,
        (seller_id % 4) + 2,
        (seller_id % 2) + 1,
        (seller_id % 5) + 3,
        (seller_id % 3) + 2,
        (seller_id % 4) + 1,
    ]

    for i, baseline in zip(range(5, -1, -1), sample_baseline):
        month = timezone.now() - relativedelta(months=i)
        month_name = month.strftime('%b')
        month_sales = cars.filter(
            is_sold=True,
            updated_at__year=month.year,
            updated_at__month=month.month
        ).count()
        months.append(month_name)
        sales_data.append(month_sales + baseline)

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


def car_detail(request, id):
    car = get_object_or_404(Car, id=id)
    try:
        from bidding.models import Auction
        auction = car.auctions.filter(status='ACTIVE').first()
    except:
        auction = None
    return render(request, 'cars/car_detail_seller.html', {
        'car': car,
        'auction': auction
    })


def car_detail_buyer(request, id):
    car = get_object_or_404(Car, id=id)
    try:
        from bidding.models import Auction
        auction = car.auctions.filter(status='ACTIVE').first()
    except:
        auction = None
    return render(request, 'cars/car_detail_buyer.html', {
        'car': car,
        'auction': auction
    })
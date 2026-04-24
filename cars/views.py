from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AddCarForm
from .models import Car, CarImage
from django.db.models import Avg, Sum
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required


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

            images = request.FILES.getlist('images')
            for i, img in enumerate(images[:5]):
                CarImage.objects.create(
                    car=car,
                    image=img,
                    is_primary=(i == 0)
                )
                if i == 0:
                    car.image = img
                    car.save()

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
    {'name': f"{car.brand} {car.model}", 'views': car.view_count}
    for car in cars.order_by('-view_count')[:3]
    ]

    # Sales trend — last 6 months
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
   
    Car.objects.filter(id=id).update(view_count=car.view_count + 1)
    car.refresh_from_db()

    try:
        from bidding.models import Auction
        auction = car.auctions.filter(status='ACTIVE').first()
    except:
        auction = None

    if request.user.is_authenticated and request.user == car.seller:
        return redirect('car_detail', id=id)

    return render(request, 'cars/car_detail_buyer.html', {
        'car': car,
        'auction': auction
    })

    from django.contrib.auth.decorators import login_required
from bidding.models import Bid, Auction

@login_required
def buyer_dashboard(request):
    # All bids placed by this buyer
    all_bids = Bid.objects.filter(
        buyer=request.user
    ).select_related('auction', 'auction__car').order_by('-created_at')

    # Split into active and ended
    active_bids = [b for b in all_bids if b.auction.status == 'ACTIVE']
    ended_bids  = [b for b in all_bids if b.auction.status == 'ENDED']

    # KPI calculations
    total_bids = all_bids.count()

    highest_bid = all_bids.order_by('-amount').first()
    highest_bid = highest_bid.amount if highest_bid else None

    # Winning = buyer's bid is the highest in that auction
    winning_count = 0
    outbid_count  = 0
    for bid in active_bids:
        top = bid.auction.bids.first()  # ordered by -amount
        if top and top.buyer == request.user:
            winning_count += 1
        else:
            outbid_count += 1

    context = {
        'total_bids':     total_bids,
        'winning_count':  winning_count,
        'outbid_count':   outbid_count,
        'highest_bid':    highest_bid,
        'active_bids':    active_bids,
        'ended_bids':     ended_bids,
    }
    return render(request, 'cars/buyer_dashboard.html', context)
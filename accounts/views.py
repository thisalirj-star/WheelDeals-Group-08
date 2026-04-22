from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomLoginForm, BuyerRegistrationForm, SellerRegistrationForm


def login_view(request):
    """
    Login page.
    After login: seller → seller_dashboard | buyer → home
    """
    # If already logged in, redirect immediately
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)

    form = CustomLoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return _redirect_by_role(user)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html', {'form': form})


def _redirect_by_role(user):
    """Helper function — redirects based on user type."""
    if user.is_seller():
        return redirect('seller_dashboard')  # Member 2 creates this
    return redirect('home')                  # Member 2 creates this


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def register_select_view(request):
    """
    Step 1 of registration.
    Shows two buttons: Register as Buyer / Register as Seller.
    """
    return render(request, 'accounts/register_select.html')


def register_buyer_view(request):
    """Step 2a — Buyer fills in their details."""
    form = BuyerRegistrationForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to WheelDeals!')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'accounts/register_buyer.html', {'form': form})


def register_seller_view(request):
    """Step 2b — Seller fills in their details including company name."""
    form = SellerRegistrationForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Seller account created!')
            return redirect('seller_dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'accounts/register_seller.html', {'form': form})


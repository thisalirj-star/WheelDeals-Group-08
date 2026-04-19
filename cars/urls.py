from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.seller_dashboard, name='dashboard'),
    path('car/<int:id>/', views.car_detail, name='car_detail'),
]
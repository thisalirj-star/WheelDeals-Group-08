from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_car_view, name='add_car'),
    path('<int:car_id>/edit/', views.edit_car_view, name='edit_car'),
    path('<int:car_id>/delete/', views.delete_car_view, name='delete_car'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('car/<int:id>/', views.car_detail, name='car_detail'),
    path('car/buyer/<int:id>/', views.car_detail_buyer, name='car_detail_buyer'),
]
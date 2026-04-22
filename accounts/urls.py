from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_select_view, name='register_select'),
    path('register/buyer/', views.register_buyer_view, name='register_buyer'),
    path('register/seller/', views.register_seller_view, name='register_seller'),
]
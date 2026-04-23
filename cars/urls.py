from django.urls import path
from django.http import HttpResponse
from . import views

# Temporary stubs so buyer_dashboard preview works
def stub(request):
    return HttpResponse("stub")

urlpatterns = [
    path('', stub, name='home'),
    path('login/', stub, name='login'),
    path('logout/', stub, name='logout'),
    path('register/', stub, name='register_select'),
    path('dashboard/', stub, name='dashboard'),
    path('car/<int:id>/', views.car_detail, name='car_detail'),
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
]
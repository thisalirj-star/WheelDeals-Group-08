from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'model', 'year', 'vehicle_type', 'starting_price', 'is_sold']
    list_filter = ['vehicle_type', 'brand', 'is_sold', 'fuel_type']
    search_fields = ['title', 'brand', 'model']
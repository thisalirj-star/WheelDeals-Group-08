from django.contrib import admin

from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'model', 'year', 'seller', 'is_sold', 'is_active')
    list_filter = ('brand', 'vehicle_type', 'fuel_type', 'is_sold')
    search_fields = ('title', 'brand', 'model', 'seller__username')


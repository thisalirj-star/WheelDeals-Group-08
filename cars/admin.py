from django.contrib import admin

from .models import Car, CarImage

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    max_num = 5

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'model', 'year', 'seller', 'is_sold', 'is_active')
    list_filter = ('brand', 'vehicle_type', 'fuel_type', 'is_sold')
    search_fields = ('title', 'brand', 'model', 'seller__username')
    inlines = [CarImageInline]

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'is_primary', 'uploaded_at')





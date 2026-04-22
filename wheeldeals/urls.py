from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# Temporary placeholder views until Member 2 builds them
def temp_home(request):
    return HttpResponse("🏠 Home page — Member 2 will build this")

def temp_dashboard(request):
    return HttpResponse("📊 Seller Dashboard — Member 2 will build this")

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('accounts.urls')),    # login at /login/, register at /register/
    path('cars/', include('cars.urls')),   # add car at /cars/add/
    path('home/', temp_home, name='home'),                    # temporary
    path('dashboard/', temp_dashboard, name='seller_dashboard'),  # temporary
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


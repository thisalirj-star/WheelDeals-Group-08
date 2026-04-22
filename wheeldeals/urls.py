from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# Temporary home placeholder until Member 4 builds it
def temp_home(request):
    return HttpResponse("🏠 Home page — coming soon")

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('accounts.urls')),    # login at /login/, register at /register/
    path('cars/', include('cars.urls')),   # add car at /cars/add/
    path('home/', temp_home, name='home'),   # temporary until Member 4 is done
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


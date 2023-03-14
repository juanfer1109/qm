from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('user/', include('users.urls')),
    path('dian/', include('dian.urls')),
    path('boletin/', include('boletin.urls')),
    path('mtto/', include('mtto.urls')),
    path('visit/', include('visit.urls')),
    path('eventos/', include('eventos.urls')),
    path('donaciones/', include('donation.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('users/', include('users.urls', namespace='users')),
    path('events/', include('events.urls', namespace='events')),
    path('tickets/', include('tickets.urls', namespace='tickets')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

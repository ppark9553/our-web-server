from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import HomeView, GatewayView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^gateway/$', GatewayView.as_view(), name='gateway'),
    url(r'^stock-api/', include('stockapi.urls', namespace='stockapi')),
    url(r'^hidden-api/', include('gateway.urls', namespace='hiddenapi')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

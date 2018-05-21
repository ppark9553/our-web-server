from django.conf.urls import include, url
from django.contrib import admin

from .views import HomeView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^stock-api/', include('stockapi.urls', namespace='stockapi')),
    url(r'^hidden-api/', include('gateway.urls', namespace='hiddenapi')),
]

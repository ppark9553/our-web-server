from django.conf.urls import url

from stockapi.views import (
    DateAPIView,
    TickerAPIView,
    OHLCVAPIView,
)

urlpatterns = [
    url(r'^date/$', DateAPIView.as_view(), name='date'),
    url(r'^ticker/$', TickerAPIView.as_view(), name='ticker'),
    url(r'^ohlcv/$', OHLCVAPIView.as_view(), name='ohlcv'),
]

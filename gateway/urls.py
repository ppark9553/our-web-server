from django.conf.urls import url

from stockapi.views import (
    DateAPIGatewayView,
    TickerAPIGatewayView,
    OHLCVAPIGatewayView,
)

urlpatterns = [
    url(r'^date/$', DateAPIGatewayView.as_view(), name='gateway-date'),
    url(r'^ticker/$', TickerAPIGatewayView.as_view(), name='gateway-ticker'),
    url(r'^ohlcv/$', OHLCVAPIGatewayView.as_view(), name='gateway-ohlcv'),
]

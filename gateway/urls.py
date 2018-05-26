from django.conf.urls import url

from gateway.views import (
    DateAPIGatewayView,
    TickerAPIGatewayView,
    OHLCVAPIGatewayView,

    GatewayStateAPIView,
    GatewayStoreView,
)

urlpatterns = [
    url(r'^date/$', DateAPIGatewayView.as_view(), name='gateway-date'),
    url(r'^ticker/$', TickerAPIGatewayView.as_view(), name='gateway-ticker'),
    url(r'^ohlcv/$', OHLCVAPIGatewayView.as_view(), name='gateway-ohlcv'),

    url(r'^gateway-states/$', GatewayStateAPIView.as_view(), name='gateway-states'),
    url(r'^task/$', GatewayStoreView.as_view(), name='gateway-store'),
]

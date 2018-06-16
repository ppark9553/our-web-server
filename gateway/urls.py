from django.conf.urls import url

from gateway.views import (
    GatewayActionAPIView,
    GatewayActionDetailsAPIView,
    GatewayStateAPIView,
    SoulLogAPIView,
    # GatewayStoreView,
)

urlpatterns = [
    url(r'^gateway-actions/$', GatewayActionAPIView.as_view(), name='gateway-actions'),
    url(r'^gateway-actions/(?P<pk>\d+)/$',GatewayActionDetailsAPIView.as_view(), name='gateway-actions-detail'),
    url(r'^gateway-states/$', GatewayStateAPIView.as_view(), name='gateway-states'),
    url(r'^soul-logs/$', SoulLogAPIView.as_view(), name='soul-logs'),
    # url(r'^task/$', GatewayStoreView.as_view(), name='gateway-store'),
]

from django.http import JsonResponse
from django.views.generic import View

from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from stockapi.models import (
    Date,
    Ticker,
    OHLCV,
)
from stockapi.serializers import (
    DateSerializer,
    TickerSerializer,
    OHLCVSerializer,
)
from gateway.models import GatewayAction, GatewayState
from gateway.serializers import GatewayActionSerializer, GatewayStateSerializer
from gateway.actions import GatewayActionOBJ
from gateway.reducers import GatewayReducer

from utils.paginations import StandardResultPagination, OHLCVPagination


class DateAPIGatewayView(generics.ListCreateAPIView):
    queryset = Date.objects.all().order_by('-date')
    serializer_class = DateSerializer
    pagination_class = StandardResultPagination


class TickerAPIGatewayView(generics.ListCreateAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Ticker.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code:
            queryset = queryset.filter(code=code_by)
        return queryset


class OHLCVAPIGatewayView(generics.ListCreateAPIView):
    queryset = OHLCV.objects.all()
    serializer_class = OHLCVSerializer
    pagination_class = OHLCVPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = OHLCV.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if start and end and not date_by:
            queryset = queryset.filter(date__gte=start).filter(date__lte=end)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


### gateway API's should be ListCreateAPIView because Node.js app
### should also be able to have access to DB writes regarding its tasks
class GatewayActionAPIView(generics.ListCreateAPIView):
    queryset = GatewayAction.objects.all().order_by('-id')
    serializer_class = GatewayActionSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]


class GatewayStateAPIView(generics.ListCreateAPIView):
    queryset = GatewayState.objects.all().order_by('-id')
    serializer_class = GatewayStateSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]


class GatewayStoreView(View):
    '''
    The GatewayStore class(object) makes an action and reduces those actions to certain results
    '''

    def get(self,request):
        # receive a type value through URL
        action_type = request.GET.get('type')
        # initialize action class by passing in the action type retrieved from URL
        action_cls = GatewayActionOBJ(action_type)
        action_obj = action_cls.ACTION
        reducer = GatewayReducer(action_obj) # pass in the action object to reducer
        return JsonResponse({'status': 'DONE'}, json_dumps_params={'ensure_ascii': True})

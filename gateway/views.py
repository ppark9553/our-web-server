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
from gateway.models import GatewayState
from gateway.serializers import GatewayStateSerializer
from gateway.actions import GatewayActionOBJ
from gateway.reducers import GatewayReducer
from gateway.logger import GatewayLogger

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
class GatewayStateAPIView(generics.ListCreateAPIView):
    queryset = GatewayState.objects.all()
    serializer_class = GatewayStateSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = GatewayState.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        task_by = self.request.GET.get('start')
        status_by = self.request.GET.get('status')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if task_by:
            queryset = queryset.filter(task_name=task_by)
        if status_by:
            queryset = queryset.filter(status=status_by)
        return queryset


class GatewayStoreView(View):
    '''
    The GatewayStore class(object) makes an action and reduces those actions to certain results
    '''

    def get(self,request):
        # create the logger
        logger = GatewayLogger()

        # receive a type value through URL
        action_type = request.GET.get('type')
        # check for action_type availability
        action_inst = GatewayActionOBJ(action_type)

        if action_inst.ACTION['type'] != 'None':
            logger.set_log(action_type, 'P', 'store received action type')

            # initialize action class by passing in the action type retrieved from URL
            action_obj = action_inst.ACTION
            reducer_inst = GatewayReducer(action_obj) # pass in the action object to reducer
            reducer_status = reducer_inst.reduce()
            if reducer_status == True:
                logger.set_log(action_type, 'P', 'action successfully reduced')
                return JsonResponse({'status': 'DONE'}, json_dumps_params={'ensure_ascii': True})
            else:
                logger.set_log(action_type, 'F', 'action failed to reduce')
                return JsonResponse({'status': 'FAIL'}, json_dumps_params={'ensure_ascii': True})

        elif action_inst.ACTION['type'] == 'None':
            logger.set_log(action_type, 'F', 'no such action exists error')
            return JsonResponse({'status': 'NO ACTION: {}'.format(action_type)}, json_dumps_params={'ensure_ascii': True})

from django.http import JsonResponse
from django.views.generic import View

from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from arbiter.config import THIS_SYSTEM
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
from gateway.models import (
    GatewayAction,
    GatewayState,
    SoulLog,
)
from gateway.serializers import (
    GatewayActionSerializer,
    GatewayStateSerializer,
    SoulLogSerializer,
)
from gateway.controllers import GatewayActionOBJ, GatewayReducer
from gateway.logger import GatewayLogger
from gateway.task_sender import TaskSender

from utils.paginations import (
    GatewayResultPagination,
    StandardResultPagination,
    OHLCVPagination,
)


### gateway API's should be ListCreateAPIView because Node.js app
### should also be able to have access to DB writes regarding its tasks
class GatewayActionAPIView(generics.ListCreateAPIView):
    queryset = GatewayAction.objects.all()
    serializer_class = GatewayActionSerializer
    pagination_class = GatewayResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = GatewayAction.objects.all().order_by('id')
        type_by = self.request.GET.get('type')
        if type_by:
            queryset = queryset.filter(type=type_by)
        return queryset


class GatewayActionDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GatewayAction.objects.all()
    serializer_class = GatewayActionSerializer


class GatewayStateAPIView(generics.ListCreateAPIView):
    queryset = GatewayState.objects.all()
    serializer_class = GatewayStateSerializer
    pagination_class = GatewayResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = GatewayState.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        task_by = self.request.GET.get('task_name')
        status_by = self.request.GET.get('status')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if task_by:
            queryset = queryset.filter(task_name=task_by)
        if status_by:
            queryset = queryset.filter(status=status_by)
        return queryset


class SoulLogAPIView(generics.ListCreateAPIView):
    queryset = SoulLog.objects.all().order_by('-id')
    serializer_class = SoulLogSerializer
    pagination_class = GatewayResultPagination
    filter_backends = [SearchFilter, OrderingFilter]


class GatewayStoreView(View):
    '''
    The GatewayStore class(object) makes an action and reduces those actions to certain results
    '''

    def get(self,request):
        # receive a type value through URL
        action_type = request.GET.get('type')

        # create the logger
        logger = GatewayLogger()

        # forward to gateway server when requested to a different server
        if THIS_SYSTEM != 'gateway':
            logger.set_log(action_type, 'P', 'requested task server not gateway, forwarding request to gateway server')
            task_sender = TaskSender(action_type)
            task_sender = task_sender.send_task(action_type)
            print('sent task')
            return JsonResponse({'status': 'FORWARDED'}, json_dumps_params={'ensure_ascii': True})
        else:
            # check for action_type availability
            action_inst = GatewayActionOBJ(action_type)

            if action_inst.action_exists():
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

            elif not action_inst.action_exists():
                logger.set_log(action_type, 'F', 'no such action exists error')
                return JsonResponse({'status': 'NO ACTION: {}'.format(action_type)}, json_dumps_params={'ensure_ascii': True})

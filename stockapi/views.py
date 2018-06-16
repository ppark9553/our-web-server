from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from stockapi.models import (
    Date,
    MarketCapital,
    BuySell,
    Ticker,
    OHLCV,
)
from stockapi.serializers import (
    DateSerializer,
    MarketCapitalSerializer,
    BuySellSerializer,
    TickerSerializer,
    OHLCVSerializer,
)

from utils.paginations import StandardResultPagination, OHLCVPagination


class DateAPIView(generics.ListAPIView):
    queryset = Date.objects.all().order_by('-date')
    serializer_class = DateSerializer
    pagination_class = StandardResultPagination


class MarketCapitalAPIView(generics.ListAPIView):
    queryset = MarketCapital.objects.all()
    serializer_class = MarketCapitalSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = MarketCapital.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class BuySellAPIView(generics.ListAPIView):
    queryset = BuySell.objects.all()
    serializer_class = BuySellSerializer
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = BuySell.objects.all().order_by('id')
        date_by = self.request.GET.get('date')
        code_by = self.request.GET.get('code')
        name_by = self.request.GET.get('name')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if code_by:
            queryset = queryset.filter(code=code_by)
        if name_by:
            queryset = queryset.filter(name=name_by)
        return queryset


class TickerAPIView(generics.ListAPIView):
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
        if code_by:
            queryset = queryset.filter(code=code_by)
        return queryset


class OHLCVAPIView(generics.ListAPIView):
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

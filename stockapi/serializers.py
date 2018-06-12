from rest_framework import serializers

from stockapi.models import (
    Date,
    MarketCapital,
    Ticker,
    OHLCV,
)


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ('date',)


class MarketCapitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketCapital
        fields = ('date',
                  'code',
                  'name',
                  'comm_cls_prc',
                  'comm_stk_qty',
                  'pref_stk_qty',
                  'comm_stk_qty_af',
                  'pref_stk_qty_af',
                  'mkt_cap_comm',
                  'mkt_cap',)


class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = ('date',
                  'code',
                  'name',
                  'market_type',
                  'state',)


class OHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = OHLCV
        fields = ('date',
                  'code',
                  'name',
                  'open_price',
                  'high_price',
                  'low_price',
                  'close_price',
                  'adj_close_price',
                  'volume',
                  'short_volume',)

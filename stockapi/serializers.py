from rest_framework import serializers

from stockapi.models import (
    Date,
    Ticker,
    OHLCV,
)


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ('date',)


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

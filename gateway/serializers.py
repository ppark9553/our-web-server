from rest_framework import serializers

from gateway.models import (
    GatewayAction,
    GatewayState,
    SoulLog,
)


class GatewayActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatewayAction
        fields = ('type',
                  'reduce',
                  'other',)


class GatewayStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatewayState
        fields = ('date',
                  'created',
                  'task_name',
                  'state',
                  'log',)


class SoulLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoulLog
        fields = ('created',
                  'log',)

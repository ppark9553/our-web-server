from rest_framework import serializers

from gateway.models import (
    GatewayAction,
    GatewayState,
)


class GatewayActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatewayAction
        fields = ('created', 'action',)
        read_only_fields = ('created',)


class GatewayStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatewayState
        fields = ('date',
                  'task_name',
                  'state',
                  'log',)

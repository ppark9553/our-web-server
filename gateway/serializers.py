from rest_framework import serializers

from gateway.models import GatewayState


class GatewayStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatewayState
        fields = ('date',
                  'created',
                  'task_name',
                  'state',
                  'log',)

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

    def create(self, validated_data):
        type = validated_data['type']
        reduce = validated_data['reduce']
        other = validated_data['other']
        action_obj = GatewayAction(
            type=type,
            reduce=reduce,
            other=other
        )
        print(type)
        print(reduce)
        print(other)
        return action_obj


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

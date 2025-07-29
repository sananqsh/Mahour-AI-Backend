from rest_framework import serializers

from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

class DashboardSerializer(serializers.Serializer):
    # {
    #     'totalOrders': 3,
    #     'totalSpent': 100,
    #     'points': 2000,
    #     'tier': 'Gold',
    #     'user': {
    #         'id': 1,
    #         'name': 'San',
    #         'tier': 'Gold',
    #         'points': 200
    #     },
    # }
    totalOrders = serializers.IntegerField()
    totalSpend = serializers.IntegerField()
    points = serializers.IntegerField()
    tier = serializers.CharField()
    user = CustomerSerializer()

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = '__all__'

from rest_framework import serializers

from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'points', 'tier')

    def get_name(self, obj):
        return obj.get_name()

class DashboardSerializer(serializers.Serializer):
    totalOrders = serializers.IntegerField()
    totalSpent = serializers.IntegerField()
    points = serializers.IntegerField()
    tier = serializers.CharField()
    user = CustomerSerializer()

class OrderSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = '__all__'

    def get_total(self, obj):
        return obj.get_total()

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = '__all__'

class OrderWithItemsSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ('id', 'user', 'date', 'total', 'items')

    def get_total(self, obj):
        return obj.get_total()

    def get_items(self, obj):
        return ProductSerializer(obj.items.all(), many=True).data

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category')

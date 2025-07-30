import json
import logging

from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import CustomUser
from dashboard.models import Order
from dashboard.serializers import DashboardSerializer, OrderSerializer
from llm_caller.services import call_llm

# Create your views here.
class DashboardView(APIView):
    serializer_class = DashboardSerializer

    def get(self, request):
        # TODO: get request.user
        user = CustomUser.objects.first()
        orders = Order.objects.filter(user=user)
        total_orders = orders.count()
        total_spent = 0
        for order in orders:
            total_spent += order.get_total()
        serializer = self.serializer_class({
            'totalOrders': total_orders,
            'totalSpent': total_spent,
            'points': user.points,
            'tier': user.tier,
            'user': user
        })
        return Response(serializer.data)


class OrdersView(APIView):
    serializer_class = OrderSerializer
    def get(self, request):
        user = CustomUser.objects.last()
        orders = Order.objects.filter(user=user)
        orders_serializer = OrderSerializer(orders, many=True)
        return Response(orders_serializer.data)


class InboxView(APIView):
    def get(self, request):
        return Response([
            {
                'id': 'i1',
                 'user_id': 1,
                 'title': 'Welcome to Gold Tier!',
                 'body': 'Congratulations! You\'ve been upgraded to Gold tier and earned 100 bonus points.',
                 'date': '2024-02-21',
                 'read_flag': False
            },
            {
                'id': 'i2',
                'user_id': 'user1',
                'title': 'Special Offer Just for You',
                'body': 'Get 20% off your next purchase of sports equipment. Use code GOLD20.',
                'date': '2024-02-18',
                'read_flag': False
            },
            {
                'id': 'i3',
                'user_id': 'user1',
                'title': 'Points Earned',
                'body': 'You earned 50 bonus points for your recent purchase!',
                'date': '2024-02-15',
                'read_flag': True
            }
        ])


class ChatView(APIView):
    def post(self, request):
        request_json = json.loads(request.body)
        logging.info(request_json)
        llm_response_message = call_llm(
            request_json.get('message'),
            "I'm a customer and you are an assistant for a customer club. Greet me and answer. "
        )

        # TODO: Add conversation_id to response
        return Response({"message": llm_response_message})

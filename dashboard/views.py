import json
import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import CustomUser
from dashboard.models import Order, Inbox
from dashboard.serializers import DashboardSerializer, OrderSerializer, InboxSerializer
from llm_caller.services import call_llm

class DashboardView(APIView):
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        orders_serializer = OrderSerializer(orders, many=True)
        return Response(orders_serializer.data)

class InboxView(APIView):
    serializer_class = InboxSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        inbox = Inbox.objects.filter(user=request.user).first()
        serializer = self.serializer_class(inbox)
        return Response(serializer.data)

class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request_json = json.loads(request.body)
        logging.info(request_json)
        llm_response_message = call_llm(
            request_json.get('message'),
            "I'm a customer and you are called Mahour AI, an assistant for a customer club. Greet me and answer. "
        )

        # TODO: Add conversation_id to response
        return Response({"message": llm_response_message})

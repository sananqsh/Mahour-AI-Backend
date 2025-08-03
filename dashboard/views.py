import json
import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from dashboard.models import Order, Inbox
from dashboard.serializers import DashboardSerializer, OrderSerializer, InboxSerializer
from dashboard.llm_utils import get_initial_context
from llm_caller.exceptions import OpenAIRequestException
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

        try:
            initial_context = get_initial_context(request.user)
            llm_response_message = call_llm(
            user_prompt=request_json.get('message'),
            history=request_json.get('history'),
            context=initial_context,
            )
        except OpenAIRequestException as e:
            print("e")
            return Response({"message": "There was an error with the request; please try again later."})

        return Response({"content": llm_response_message})

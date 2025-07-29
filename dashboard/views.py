from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class DashboardView(APIView):
    def get(self, request):
        return Response({
            'totalOrders': 3,
            'totalSpent': 100,
            'points': 2000,
            'tier': 'Gold',
            'user': {
                'id': 1,
                'name': 'San',
                'tier': 'Gold',
                'points': 200
            },
        })


class OrdersView(APIView):
    def get(self, request):
        return Response([
            {
                'id': 1,
                'date': datetime.now(),
                'created_at': datetime.now(),
                'items': [
                    {
                        'product_id': 1,
                        'quantity': 1,
                        'price': 100,
                    },
                    {
                        'product_id': 2,
                        'quantity': 2,
                        'price': 20,
                    }
                ],
                'total': 140,
            },
            {
                'id': 2,
                'date': datetime.now(),
                'created_at': datetime.now(),
                'items': [
                    {
                        'product_id': 3,
                        'quantity': 1,
                        'price': 50,
                    }
                ],
                'total': 50,
            }
        ])

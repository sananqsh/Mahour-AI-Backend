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

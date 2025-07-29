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

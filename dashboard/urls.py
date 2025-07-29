from django.urls import path
from .views import DashboardView, OrdersView

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('orders', OrdersView.as_view(), name='orders'),
]

from django.urls import path
from .views import DashboardView, OrdersView, InboxView, ChatView

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('orders', OrdersView.as_view(), name='orders'),
    path('inbox', InboxView.as_view(), name='inbox'),
    path('chat', ChatView.as_view(), name='chat'),
]

from django.contrib.auth.decorators import login_required
from django.urls import path

from orders.views import (CanceledTemplateView, OrderCreateView,
                          OrderDetailView, OrderListView, SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('order_create/', login_required(OrderCreateView.as_view()), name='order_create'),
    path('', login_required(OrderListView.as_view()), name='orders_list'),
    path('order/<int:pk>/', login_required(OrderDetailView.as_view()), name='order'),
    path('order_success/', login_required(SuccessTemplateView.as_view()), name='order_success'),
    path('order_canceled/', login_required(CanceledTemplateView.as_view()), name='order_canceled'),
]

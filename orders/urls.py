from django.urls import path

from orders.views import (CanceledTemplateView, OrderCreateView,
                          OrderDetailView, OrderListView, SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('order_success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order_canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]

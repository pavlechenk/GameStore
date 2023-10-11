from django.urls import path

from orders.views import OrderCreateView, SuccessTemplateView, CanceledTemplateView

app_name = 'orders'

urlpatterns = [
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order_success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order_canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
]

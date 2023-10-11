import stripe
from django.http import HttpResponseRedirect
from http import HTTPStatus
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.conf import settings
from common.views import TitleMixin
from orders.forms import OrderForm


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    title = 'GameStore - Спасибо за заказ!'
    template_name = 'orders/success.html'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderCreateView(TitleMixin, CreateView):
    title = 'GameStore - Оформление заказа'
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NzrSoKhAHe2VHlF4fe9hfAa',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)

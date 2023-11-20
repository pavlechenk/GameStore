from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from games.models import Basket
from orders.forms import OrderForm
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    title = 'GameStore - Спасибо за заказ!'
    template_name = 'orders/success.html'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):
    title = 'GameStore - Заказы'
    template_name = 'orders/orders.html'
    model = Order
    context_object_name = 'orders'
    ordering = ('created',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_numbers'] = list(range(1, Order.objects.filter(initiator=self.request.user).count() + 1))
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'GameStore - Заказ №{self.object.id}'
        return context


class OrderCreateView(TitleMixin, CreateView):
    title = 'GameStore - Оформление заказа'
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        Order.objects.get(id=self.object.id).update_before_payment()
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_games(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=HTTPStatus.BAD_REQUEST)

        # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

        # Passed signature verification
    return HttpResponse(status=HTTPStatus.OK)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()

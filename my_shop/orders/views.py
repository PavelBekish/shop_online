from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from shop.utils import DataMixin
from .models import OrderItem, Order
from shop.models import Product
from .forms import OrderCreateForm
from cart.cart import Cart
from .serializers import OrderSerializer, OrderItemSerializer
from .tasks import order_created


class OrderCreate(DataMixin, TemplateView):

    template_name = 'orders/order/create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        form = OrderCreateForm
        context = super().get_context_data(**kwargs)
        context['form'] = form
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class OrderCreated(DataMixin, TemplateView):
    template_name = 'orders/order/created.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        cart = Cart(self.request)
        form = OrderCreateForm(self.request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.promocode:
                order.promocode = cart.promocode
                order.discount = cart.promocode.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

                prod = Product.objects.get(pk=item['product'].id)
                prod.stock = prod.stock - item['quantity']
                if prod.stock == 0:
                    prod.available = False
                prod.save()

            cart.clear()
            order_created.delay(order.id)
            context['order'] = order
            return self.render_to_response(context)
        else:
            context = form.errors.as_data()
            context['form'] = form
            return render(request, 'orders/order/create.html', context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class OrderAPIList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from shop.models import Product
from shop.utils import DataMixin
from .cart import Cart
from .forms import CartAddProductForm
from promocodes.forms import PromoCodeApplyForm


@require_POST
def cart_add(request):
    return_dict = dict()
    cart = Cart(request)
    data = request.POST
    product_id = data.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product,)
    return_dict['total_items'] = len(cart)
    return JsonResponse(return_dict)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


class CartDetail(DataMixin, TemplateView):
    template_name = 'cart/detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = Cart(self.request)
        promocode_apply_form = PromoCodeApplyForm()
        context = super().get_context_data(**kwargs)
        context['promocode_apply_form'] = promocode_apply_form
        context['cart'] = cart
        context['empty_cart'] = True if len(cart) == 0 else False
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))
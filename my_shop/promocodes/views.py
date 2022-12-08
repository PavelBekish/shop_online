from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import PromoCode
from .forms import PromoCodeApplyForm


@require_POST
def promocode_apply(request):
    now = timezone.now()
    form = PromoCodeApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            promocode = PromoCode.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['promocode_id'] = promocode.id
        except ObjectDoesNotExist:
            request.session['promocode_id'] = None
    return redirect('cart_detail')
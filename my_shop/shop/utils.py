from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import CategoryGroup, Product, Manufacturer


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        category_groups = cache.get('category_groups')
        if not category_groups:
            category_groups = CategoryGroup.objects.prefetch_related('categories')
            cache.set('category_groups', category_groups, 180)
        context['category_groups'] = category_groups

        return context

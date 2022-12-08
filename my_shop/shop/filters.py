import django_filters
from django_filters import BaseInFilter, NumberFilter, FilterSet
from shop.models import Product


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class ProductFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super(ProductFilter, self).__init__(*args, **kwargs)
        self.data = dict(self.data)
        for key, value in self.data.items():
            self.data[key] = ", ".join(value)

    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    manufacturer = NumberInFilter(field_name='manufacturer__id', lookup_expr='in')

    class Meta:
        model = Product
        fields = ['price_from', 'price_to', 'manufacturer']

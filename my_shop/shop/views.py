from django.views.generic import ListView, DetailView, TemplateView
from rest_framework import generics
from .filters import ProductFilter
from .serializers import ProductSerializer
from .utils import DataMixin
from .models import Category, Product, CategoryGroup, Manufacturer
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


class HomePage(TemplateView):
    template_name = 'shop/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_groups'] = CategoryGroup.objects.prefetch_related('categories', 'products')

        return dict(list(context.items()))


class ProductDetail(DataMixin, DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class ProductCategory(DataMixin, ListView):
    paginate_by = 5
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_queryset(self):

        if 'category_slug' in self.kwargs:
            category_products = Product.objects.filter(category__slug=self.kwargs['category_slug'])
            filter_products = ProductFilter(self.request.GET, category_products)
            return filter_products.qs
        else:
            category_group_products = Product.objects.filter(category__category_group__slug=
                                                             self.kwargs['category_group_slug'])
            filter_products = ProductFilter(self.request.GET, category_group_products)
            return filter_products.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filters = ''
        for key, values in dict(self.request.GET).items():
            if key != 'page':
                filters = ''.join(f"{key}={value}&" for value in values)

        context['filters'] = filters
        if 'category_slug' in self.kwargs:
            category = Category.objects.select_related('category_group').get(slug=self.kwargs['category_slug'])
            context['category'] = category
            context['max_price'] = Product.objects.values('price').filter(
                category__slug=self.kwargs['category_slug']).order_by('-price').first()
        else:
            category_group = CategoryGroup.objects.get(slug=self.kwargs['category_group_slug'])
            context['category_group'] = category_group
            context['max_price'] = Product.objects.values('price').filter(
                category__category_group__slug=self.kwargs['category_group_slug']).order_by('-price').first()
        context['manufacturers'] = Manufacturer.objects.all()
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class Search(DataMixin, ListView):
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        search_vector = SearchVector('name', weight='A') + SearchVector('description', weight='B')
        search_query = SearchQuery(query)
        # weight A, B, C, D - 1.0, 0.4, 0.2, 0.1
        results = Product.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)
                                           ).filter(rank__gte=0.3).order_by('-rank')
        return results

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = f"q={self.request.GET.get('q')}&"
        c_def = self.get_user_context(title=context['products'])
        return dict(list(context.items()) + list(c_def.items()))


class ProductAPIListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

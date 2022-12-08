from django.urls import path
from shop import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('api/v1/productlist/', views.ProductAPIListCreate.as_view()),
    path('api/v1/createproduct/', views.ProductAPIListCreate.as_view()),
    path('search', views.Search.as_view(), name='search'),
    path('product_deteil/<slug:product_slug>', views.ProductDetail.as_view(), name='product_detail'),
    path('<slug:category_group_slug>', views.ProductCategory.as_view(), name='category_group'),
    path('<slug:category_group_slug>/<slug:category_slug>', views.ProductCategory.as_view(), name='category'),
]

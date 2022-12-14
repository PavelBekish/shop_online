from django.urls import re_path, path
from . import views


urlpatterns = [
    path('', views.CartDetail.as_view(), name='cart_detail'),
    path('add/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]
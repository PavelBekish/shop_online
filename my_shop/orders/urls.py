from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.OrderCreate.as_view(), name='order_create'),
    path('created/', views.OrderCreated.as_view(), name='order_created'),
    path('api/v1/orderlist/', views.OrderAPIList.as_view()),
]
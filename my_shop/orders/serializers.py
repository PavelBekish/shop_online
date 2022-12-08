from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    OrderItems = serializers.SerializerMethodField('get_items')

    # Функция возвращает товары заказа
    def get_items(self, Order):
        items = OrderItem.objects.filter(order__pk=Order.pk)
        items_serialized = OrderItemSerializer(items, many=True)
        return items_serialized.data

    class Meta:
        model = Order
        fields = '__all__'


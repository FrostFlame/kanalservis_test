from rest_framework import serializers

from web.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор модели заказа."""

    class Meta:
        model = Order
        fields = ('order_number', 'date', 'price_dol', 'price_rub')

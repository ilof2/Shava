from rest_framework import serializers

from shava.models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            'id',
            'message',
            'product_id',
            'phone_number',
            'address',
            'customer_name',
            'price',
        )
import json

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from shava.models import Order, Product


class CreateOrder(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        phone = data.get("phone")
        name = data.get("name")
        address = data.get("address")
        message = data.get("message")
        products_data = json.loads(request.data.get("products", '{}'))
        product_ids = products_data.keys()
        product_objs = Product.objects.filter(id__in=product_ids)
        order = Order(address=address, message=message, phone_number=phone, customer_name=name)
        order.save()
        for prod in product_objs:
            order.product.add(prod)
        order.save()
        return Response(status=200)

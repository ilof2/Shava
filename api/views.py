import json

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from shava.models import Order, Product, OrderProductCount


class CreateOrder(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        response = validation(data)
        if response.status_code != 200:
            return response
        phone = data.get("phone")
        name = data.get("name")
        address = data.get("address")
        message = data.get("message")
        products_data = json.loads(request.data.get("products", '{}'))
        product_ids = products_data.keys()
        product_objs = Product.objects.filter(id__in=product_ids)
        order = Order(address=address, message=message, phone_number=phone, customer_name=name, price=0)
        for prod in products_data.values():
            order.price = order.price + (prod.get("price", 0) * prod.get("count"))

        try:
            order.save()
        except Exception:
            Response(status=500)

        for prod in product_objs:
            order.product.add(prod)
        try:
            order.save()
        except Exception:
            Response(status=500)
        for prod_id, prod in products_data.items():
            order_count = OrderProductCount(product_id=prod_id, order_id=order.id, count=prod.get("count"))
            try:
                order_count.save()
            except Exception:
                Response(status=500)
        return Response(status=200)


def validation(data):
    if data.get("phone") and data.get("name") and data.get("address") and data.get("message"):
        return
    if len(data.get("message")) > 200:
        return Response(status=400)
    return Response(status=400)

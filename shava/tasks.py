from .celery import app
import requests
from .settings import CHAT_ID, BOT_TOKEN
from .models import Order
from django.utils import timezone
from .settings import ORDER_LIVING_TIME


@app.task
def send_message_order():
    not_sended_orders = Order.objects.filter(is_sended=False)
    order_status = {'PENDING': 'В ОЖИДАНИИ!', 'PROCESSED': 'В ОЖИДАНИИ'}
    for order in not_sended_orders:
        if len(order.product.all()) == len(order.order_product_counter.all()) and len(order.product.all()):
            product_list = '\n'
            for product in order.order_product_counter.all():
                product_list = f"{product_list} {product.product.name} : {product.count} \n"
            text = f'Заказ:\nИмя Клиента: {order.customer_name}\n' \
            f'Номер Клиента: {order.phone_number}\n' \
            f'Адресс: {order.address}\n' \
            f'Статус: {order_status[order.status]}\n' \
            f'Товары: {product_list}\n' \
            f'Комментарий к заказу: {order.message}\n' \
            f'Общая цена: {order.price} Р'
            params = {'chat_id': CHAT_ID, 'text': text}
            requests.post(BOT_TOKEN + 'sendMessage', data=params)
            order.is_sended = True
            order.save()


@app.task
def delete_not_sended_orders():
    not_sended_orders = Order.objects.filter(is_sended=False)
    for order in not_sended_orders:
        delta = (timezone.now() - order.created_at).seconds
        if delta > ORDER_LIVING_TIME:
            order.delete()





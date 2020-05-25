from PIL import Image
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from .tasks import send_message_order


class Category(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name="Категория")

    class Meta:
        default_related_name = 'category'
        db_table = 'category'
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Product(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name="Товар")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Категория")
    description = models.TextField(max_length=200, blank=True, verbose_name="Описание")
    image = models.ImageField(height_field=None, width_field=None)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")

    class Meta:
        default_related_name = 'product'
        db_table = 'product'
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'

    def __str__(self):
        return self.name


class Order(models.Model):

    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", _("В ОЖИДАНИИ")
        PROCESSED = "PROCESSED", _("ОБРАБОТАН")

    id = models.AutoField(primary_key=True,)
    message = models.TextField(max_length=200, blank=True, verbose_name="Коментарий к заказу")
    product = models.ManyToManyField('Product', related_name='orders', verbose_name="Товара")
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING, verbose_name="Статус заказа")
    phone_number = models.CharField(max_length=13, verbose_name="Телефон")
    address = models.CharField(max_length=100, verbose_name="Адресс")
    customer_name = models.CharField(max_length=50, verbose_name="Имя клиента")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.customer_name

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


@receiver(m2m_changed, sender=Order.product.through)
def email_sending_order(sender, instance, **kwargs):
    order_status = {'PENDING': 'В ОЖИДАНИИ!'}
    products = []

    for product in instance.product.all():
        products.append(product.name)
    if products:
        text = f'Заказ:\nИмя Клиента: {instance.customer_name}\n' \
               f'Номер Клиента: {instance.phone_number}\n' \
               f'Адресс: {instance.address}\n' \
               f'Статус: {order_status[instance.status]}\n' \
               f'Товары: {", ".join(products)}\n' \
               f'Комментарий к заказу: {instance.message}\n' \
               f'Общая цена: {instance.price} Р'
        send_message_order.delay(text)




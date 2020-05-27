from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


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
    is_sended = models.BooleanField(default=False)
    product = models.ManyToManyField('Product', related_name='orders', verbose_name="Товара")
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING, verbose_name="Статус заказа")
    phone_number = models.CharField(max_length=13, verbose_name="Телефон")
    address = models.CharField(max_length=100, verbose_name="Адресс")
    customer_name = models.CharField(max_length=50, verbose_name="Имя клиента")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True)

    def product_list(self):
        product_list = ''
        for product in OrderProductCount.objects.filter(order__pk=self.pk):
            product_list = f"</br>{product_list} <p>{product.product.name}: {product.count}</p>"
        return format_html(product_list)

    def get_products_for_message(self):
        product_list = ''
        for product in OrderProductCount.objects.filter(order__pk=self.pk):
            product_list = f"{product_list} {product.product.name} : {product.count} \n"
        return product_list

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


class OrderProductCount(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()

    class Meta:
        default_related_name = 'order_product_counter'
        db_table = 'order_product_counter'


from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    class Meta:
        default_related_name = 'category'
        db_table = 'category'
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name


class Product(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(max_length=200, blank=True)
    image = models.ImageField(upload_to='uploads/', height_field=None, width_field=None)
    price = models.IntegerField(default=0)

    class Meta:
        default_related_name = 'product'
        db_table = 'product'
        verbose_name_plural = 'Product'

    def __str__(self):
        return self.name


class Order(models.Model):

    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", _("В ОЖИДАНИИ")
        PROCESSED = "PROCESSED", _("ОБРАБОТАН")

    id = models.AutoField(primary_key=True)
    message = models.TextField(max_length=200, blank=True)
    product = models.ManyToManyField('Product', blank=True, related_name='orders')
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    phone_number = models.CharField(max_length=13)
    address = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.customer_name



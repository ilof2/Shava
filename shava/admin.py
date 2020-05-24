from .models import *
from django.contrib import admin


admin.site.site_title = 'Platform 1'
admin.site.site_header = 'Platform 1'
admin.site.site_index = 'Platform 1'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_editable = ('name', 'price')
    search_fields = ('name',)
    readonly_fields = ('id', )
    list_filter = ('name', 'price', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_editable = ('name', )
    search_fields = ('name', )
    readonly_fields = ('id',)
    list_filter = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'phone_number', 'customer_name', 'price')
    list_editable = ('status',)
    search_fields = ('customer_name', 'phone_number')
    readonly_fields = ('id',)
    list_filter = ('status', 'phone_number')

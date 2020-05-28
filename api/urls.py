from django.urls import path

from api.views import CreateOrder

urlpatterns = [
    path('order/create/', CreateOrder.as_view(), name='create_order')
]


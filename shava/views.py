from django.shortcuts import render
from .models import Product, Category


def index(request):
    return render(
        request,
        "index.html",
        context={"products": Product.objects.all(), "categories": Category.objects.all()}
    )

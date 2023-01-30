from django.urls import re_path

# from django.urls import path
from . import views

urlpatterns = [
    re_path(r"^api/v1/product/(?P<pk>[0-9]+)$", views.get_product, name="get_product"),
    re_path(
        r"^order/api/v1/products/(?P<search>[a-zA-Z]*)$",
        views.get_products,
        name="get_products",
    ),
    re_path(
        r"^api/v1/product/$",
        views.get_update_product_by_code,
        name="get_update_product_by_code",
    ),
    re_path(r"^api/v1/product/create$", views.post_product, name="post_product"),
]

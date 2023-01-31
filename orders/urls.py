from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r"^order/$", views.order_page, name="order_page"),
    re_path(r"^order/api/v1/orderconfirmation", views.order_product, name="order"),
    re_path(
        r"^order/invoice/(?P<filename>[a-zA-Z0-9_\-\. ]+)$",
        views.invoice_pdf,
        name="invoice",
    ),
    path("", views.index, name="index"),
    path("products", views.index, name="index"),
    path("landing-page", views.landing_page, name="landing_page"),
]

from django.conf.urls import url 
from django.urls import path
from . import views

urlpatterns = [
    url(
        r'^order/$',
        views.order_page,
        name='order_page'
    ),
    url(
        r'^order/api/v1/orderconfirmation',
        views.order_product,
        name="order"
    ),  
    url(
        r'^order/invoice/(?P<filename>[a-zA-Z0-9_\-\. ]+)$',
        views.invoice_pdf, 
        name="invoice"
        ),
    path("", views.index, name="index"),
    path("products", views.index, name="index"),
]
from django.db import models
from products.models import Product


class Order(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.TextField()
    phone = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    row_status = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

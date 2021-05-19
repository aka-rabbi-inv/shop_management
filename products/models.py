from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    #id = models.PositiveSmallIntegerField(primary_key=True)
    id = models.AutoField(primary_key=True)
    # mess_id = models.PositiveIntegerField()
    product_code = models.IntegerField(unique=True)
    product_name = models.CharField(max_length=50)
    product_category = models.CharField(max_length=20) 
    unit_price = models.FloatField(validators=[MinValueValidator(0)])
    current_stock = models.IntegerField(validators=[MinValueValidator(0)])
    row_status = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
       return self.product_name
    
class CustomerOrder(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.TextField()
    phone = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(max_length=200,blank=True, null=True)
    quantity = models.PositiveIntegerField()
    row_status = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
        
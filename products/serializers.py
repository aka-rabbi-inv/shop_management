from rest_framework import serializers 
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = ('product_code', 'product_name', 'product_category', 'unit_price', 'current_stock', 'row_status')
        
class ProductSerializerForPatch(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = ('unit_price','current_stock')
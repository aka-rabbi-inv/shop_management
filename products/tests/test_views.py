import json
from ..models import Product
from rest_framework import status
from django.urls import reverse
from django.test import TestCase, Client
from ..serializers import ProductSerializer

client = Client()

class GetSingleProductTest(TestCase):

    def setUp(self):

        self.product = Product.objects.create(
            product_code = 0,
            product_name = 'test product',
            product_category = 'sports',
            unit_price = 420.00,
            current_stock=1, 
            row_status = 1
        )

     

    def test_get_valid_product(self):
        response = client.get(
            reverse('get_update_product_by_code'),
            **{'HTTP_PRODUCT_CODE':self.product.product_code},
        )

        product = Product.objects.get(product_code=self.product.product_code)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_user_product_with_pk(self):
        response = client.get(
            reverse('get_product', kwargs={'pk':self.product.pk})
        )

        product = Product.objects.get(pk=self.product.pk)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class DeleteSingleProduct(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            product_code = 0,
            product_name = 'test product',
            product_category = 'sports',
            unit_price = 420.00,
            current_stock=1,
            row_status = 1
        )

    def test_single_d_delete_by_pk(self):
        response = client.delete(
            reverse('get_product', kwargs={'pk':self.product.pk},)
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class UpdateSingleProduct(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            product_code = 0,
            product_name = 'test product',
            product_category = 'sports',
            unit_price = 420.00,
            current_stock=1,
            row_status = 1
        )
        self.valid_payload = {
            "unit_price":400.00,
            "current_stock": 120
        }
        self.invalid_payload = {
            "current_stock":1
        }   

    def test_update_single_valid_product_by_pk(self):

        response = client.patch(
            reverse('get_product', kwargs={'pk':self.product.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_single_invalid_product_by_pk(self):

        response = client.patch(
            reverse('get_product', kwargs={'pk':self.product.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
    def test_update_single_valid_product_by_code(self):
        extras = {'HTTP_PRODUCT_CODE':self.product.product_code}
        response = client.patch(
            reverse('get_update_product_by_code'),
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            **extras,
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_single_invalid_product_by_code(self):
        extras = {'HTTP_PRODUCT_CODE':self.product.product_code}
        response = client.patch(
            reverse('get_update_product_by_code'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json',
            **extras
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class CreateSingleProduct(TestCase):
    
    def setUp(self):
        
        self.valid_payload = {
            "product_code" : 101,
            "product_name" : 'new product',
            "product_category" : 'home',
            "unit_price" : 1000.00,
            "current_stock":1,
            "row_status" : 1
        }

    def test_create_product(self):
        
        response = client.post(
            reverse('post_product'),
            data=json.dumps(self.valid_payload),
            content_type='Application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

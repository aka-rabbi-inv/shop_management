from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer, ProductSerializerForPatch
from django.contrib.auth.decorators import login_required


@api_view(["GET"])
@login_required
def get_products(request, search):
    """
    returns all data or data that matches the "search" substring
    """
    if request.method == "GET":
        if search:
            products = Product.objects.filter(product_name__startswith=search)
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(["GET", "DELETE", "PATCH"])
@login_required
def get_product(request, pk):

    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)

    if request.method == "GET":
        return Response(serializer.data)

    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PATCH":
        serializer = ProductSerializerForPatch(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH"])
@login_required
def get_update_product_by_code(request):
    """
    reads or updates product. product_code is passed in the header
    """
    product_code = request.META.get("HTTP_PRODUCT_CODE")

    try:
        product = Product.objects.get(product_code=product_code)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Product.MultipleObjectsReturned:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = ProductSerializer(product)

    if request.method == "GET":
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = ProductSerializerForPatch(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@login_required
def post_product(request):
    """
    creates a product.
    """
    if request.method == "POST":

        data = {
            "product_code": int(request.data.get("product_code")),
            "product_name": request.data.get("product_name"),
            "product_category": request.data.get("product_category"),
            "unit_price": float(request.data.get("unit_price")),
            "current_stock": int(request.data.get("current_stock")),
            "row_status": request.data.get("row_status"),
        }
        try:
            serializer = ProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

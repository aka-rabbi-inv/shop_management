from django.shortcuts import render
from products.models import Product, CustomerOrder
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from orders import invoice
import os
from django.http import FileResponse
from django.http import JsonResponse
from django.urls import reverse
from shop_management.settings import BASE_DIR

# Create your views here.


class OutofStockError(Exception):
    # __str__ is used to debug the exception
    def __str__(self):
        return "There is not enough stock!"


def order_page(request):
    """
    Renders order page.
    """
    return render(request, "orders/order.html")


def index(request):
    products = Product.objects.all()
    return render(request, "orders/index.html", {"products": products})


@api_view(["POST"])
def order_product(request):
    """
    Handles the order submission.
    """
    if request.method == "POST":
        data = {
            "name": request.data.get("name"),
            "phone": request.data.get("phone"),
            "email": request.data.get("email"),
            "product_detail": request.data.get("product_detail"),
        }
        products = {}
        # validation for product availability
        for content in data["product_detail"]:
            try:
                quantity = content["quantity"]
                product = Product.objects.get(product_code=content["product_code"])
                if content["product_code"] not in products:
                    products[content["product_code"]] = int(quantity)
                else:
                    products[content["product_code"]] += int(quantity)
                if int(products[content["product_code"]]) > product.current_stock:
                    raise OutofStockError

            except Product.DoesNotExist:
                return JsonResponse(
                    {"error": f"No product with name {content['product_name']}."},
                    status=406,
                )
            except OutofStockError:
                return JsonResponse(
                    {
                        "error": f"Out of stock. Currently have {product.current_stock} units of {product.product_name}."
                    },
                    status=406,
                )
        # creat customer orders and set the new stock amount
        for code, quant in products.items():
            product = Product.objects.get(product_code=code)
            product.current_stock = product.current_stock - int(quant)
            product.save()
            CustomerOrder.objects.create(
                products=product,
                name=data["name"],
                phone=data["phone"],
                email=data["email"],
                quantity=quant,
                row_status=1,
            )

        # making the qrcode for the order
        filename = invoice.product(data)
        # remove qrcode image after making pdf file
        os.remove(os.path.splitext(filename)[0] + ".png")

        return JsonResponse({"filename": filename}, status=201)


def invoice_pdf(request, filename):
    """renders the invoice pdf upon valid order"""
    file_path = os.path.join(BASE_DIR, filename)
    pdf = open(file_path, "rb")

    response = FileResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'filename="invoice.pdf"'

    return response

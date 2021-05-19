## How to Install

Python 3.8 and pipenv:
```bash
$ sudo apt install pipenv
```
inside the project folder run-
```bash
$ pipenv shell
$ pipenv install --ignore-pipfile
# will install all required packages from pipfile.lock
```

## start server
if you want to test on a computer connected on the same network navigate to settings.py file and rewrite this line
```python
ALLOWED_HOSTS = ['127.0.0.1','<YOUR HOST PC IP HERE>']
```
start the server using 
```bash
$ python manage.py runserver 0.0.0.0:8000
```
otherwise you can just test on localhost by 
```bash
$ python manage.py runserver
```

## Usage

Start by navigating to http://IP:8000 (replace IP with your ip or localhost). You can see a list of products that are already created. You can edit or delete these products clicking the respective icons. The edit form will only allow you to update the price and current stock. The delete button will require a confirmation to delete the product.
  
Navigate to Add Product by clicking the button. You can't put negative values in price and current stock as you will recieve a 400 status from the api. Try creating a product by filling all the fields.
  
You can always go to home page by clicking on the header text.
  
Now navigte to New Order page. You can pick products using the dropdown in the search field. Add more of these fields by pressing "+" if you want multiple products. Select the quantity and write customer details and press order. If the form is valid you will be redirected to a invoice pdf that will have customer information( in qrcode) and the order details. You can choose to download this pdf or back out.*
An example screenshot of the invoice is given below-
  
  
<img height="600" src="https://raw.githubusercontent.com/aka-rabbi/shop_management/main/invoice.png">
  
You can check out the customer orders afterwards by visiting the admin page at  http://IP:8000/admin
user- aka
pass- aaaa0000
You can check out the tests at products/tests/test_views.py.
  
\* Limitation- currently the invoice pdfs stack up on the project root folder. In future i might add a page to delete/view the pdfs.
 

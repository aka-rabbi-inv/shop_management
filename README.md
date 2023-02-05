## How to Install

You need Python 3.8 and pipenv

inside the project folder run-

```bash
pipenv shell
pipenv install
```

## Auth0

This project uses auth0 for authentication

get your app credentials following this [page](https://auth0.com/docs/quickstart/webapp/django/01-login#configure-auth0)

and add them to

```python
# Auth0 settings
SOCIAL_AUTH_AUTH0_DOMAIN = "fake"
SOCIAL_AUTH_AUTH0_KEY = "fake"
SOCIAL_AUTH_AUTH0_SECRET = "fake"
```

in `settings.py`

## start server

Migrate database using

```bash
python manage.py migrate
```

You might need to add your IP in the allowed hosts list in `settings.py` if you're having trouble with the connection

```python
ALLOWED_HOSTS = ['127.0.0.1','<YOUR HOST PC IP HERE>']
```

start the server using

```bash
python manage.py runserver 0.0.0.0:8000
```

you can just test on localhost by

```bash
python manage.py runserver
```

## Docker

make sure to create a .env file following the .env.fake file in the repo. This will create a superuser using the env variables.

```bash
docker build . -t shop_management:latest
```

```bash
docker run --env-file .env -p 8000:8000 -it shop_management:latest
```

## Usage

Log in to admin panel using http://{host}:8000/admin. (replace `host` with your ip or localhost). You can cerate a super user following [this command](#admin-panel-optional). Then navigate to http://{host}:8000. You need to add some products.

Navigate to Add Product by clicking the button. You can't put negative values in price and current stock as you will recieve a 400 status from the api. Try creating some products by filling all the fields. Then log out.

Now log in to the app using the login button. You can use a google account to login. An user with 'employee' role will automatically be created as you log in. A new user does not have permission to add a new product but they can place orders.

You can see a list of products in the home page. You can edit or delete these products clicking the respective icons. The edit form will only allow you to update the price and current stock. The delete button will require a confirmation to delete the product.

You can always go to home page by clicking on the home icon.

Now navigte to New Order page. You can pick products using the dropdown in the search field. Add more of these fields by pressing "+" if you want multiple products. Select the quantity and write customer details and press order. If the form is valid you will be redirected to a invoice pdf that will have customer information( in qrcode) and the order details. You can choose to download this pdf or back out.\*
An example screenshot of the invoice is given below-

<img height="600" src="https://raw.githubusercontent.com/aka-rabbi/shop_management/main/invoice.png">

## Admin Panel( Optional)

create a superuser for your project using

```bash
python manage.py createsuperuser
```

You can check out the customer orders afterwards by visiting the admin page at http://{host}:8000/admin and providing the superuser id and password.

## Tests

You can also check out the tests at products/tests/test_views.py.
\
\
\
\* Limitation- currently the invoice pdfs stack up on the project root folder. In future i might add a page to delete/view the pdfs.

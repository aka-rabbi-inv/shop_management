from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    pass


@receiver(post_save, sender=User)
def initiate_user(sender, instance, created, **kwargs):
    if created:
        employee_group, gruop_created = Group.objects.get_or_create(name="Employee")
        if gruop_created:
            employee_group.permissions.add(Permission.objects.get(name="Can add order"))
        employee_group.user_set.add(instance)
        Token.objects.create(user=instance)


class Product(models.Model):
    class Meta:
        permissions = (
            ("see_product_create_form", "Can see the form to create new product"),
        )

    id = models.AutoField(primary_key=True)
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

from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from django.conf import settings
from django.contrib import admin
from uuid import uuid4

from .validators import validate_integers, validate_file_size

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class FoodItem(models.Model):
    VEG = 'V'
    NON_VEG = 'NV'
    FOOD_TYPE = [
        (VEG, 'Veg'),
        (NON_VEG, 'Non-Veg')
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField()
    type = models.CharField(max_length=2, choices=FOOD_TYPE, default=VEG)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='fooditems')

    def __str__(self) -> str:
        return self.title


class FoodImage(models.Model):
    image = models.ImageField(upload_to='food_store/images', validators=[validate_file_size])
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='images')


class Customer(models.Model):
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10), validate_integers])
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.PositiveIntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='address')


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, 
        choices=PAYMENT_STATUS_CHOICES, 
        default=PAYMENT_STATUS_PENDING
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    # total_amount = models.PositiveIntegerField()

    # def total_amount(self):
    #     total_amount = 0
    #     for items in self.orderitems.all():
    #         total_amount += items.quantity * items.unit_price
    #     return total_amount


class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='orderitems')
    fooditem = models.ForeignKey(FoodItem, on_delete=models.PROTECT)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['cart', 'fooditem']]

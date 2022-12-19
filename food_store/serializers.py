from django.forms import ValidationError
from django.db import transaction
from rest_framework import serializers
from .models import Address, Cart, CartItem, Category, Customer, FoodImage, FoodItem, Order, OrderItem


# -- CATEGORY -- #
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'fooditems_count']
    
    fooditems_count = serializers.IntegerField(read_only=True)


class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImage
        fields = ['id', 'image']

    def create(self, validated_data):
        fooditem_id = self.context['fooditem_id']
        return FoodImage.objects.create(food_item_id=fooditem_id, **validated_data)


# -- FOODITEM -- #
class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'title', 'description', 'type', 'unit_price', 'category', 'images']
    
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    images = FoodImageSerializer(many=True, read_only=True)


class UpdateFoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['title', 'description', 'unit_price']


class SimpleFoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'title', 'type', 'unit_price']


# -- CARTITEM -- #
class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['id', 'fooditem', 'quantity', 'total_price']
    
    fooditem = SimpleFoodItemSerializer()
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self, cartitem: CartItem):
        return cartitem.quantity * cartitem.fooditem.unit_price


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['fooditem_id', 'quantity']

    fooditem_id = serializers.IntegerField()
    
    def validate_fooditem_id(self, value):
        if not FoodItem.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No fooditem with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        fooditem_id = self.validated_data['fooditem_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, fooditem_id=fooditem_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance  = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance
        

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


# -- CART -- #
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'cartitems', 'total_cart_price']
    
    cartitems = CartItemSerializer(many=True, read_only=True)
    total_cart_price = serializers.SerializerMethodField(method_name='calculate_cart_price')

    def calculate_cart_price(self, cart: Cart):
        return sum([items.quantity * items.fooditem.unit_price for items in cart.cartitems.all()])


# -- ORDER -- #
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'unit_price', 'fooditem']
    
    fooditem = serializers.StringRelatedField()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer', 'orderitems', 'total_items', 'total_price']
    
    orderitems = OrderItemSerializer(many=True, read_only=True)
    customer = serializers.StringRelatedField()
    total_items = serializers.SerializerMethodField('calculate_total_items')
    total_price = serializers.SerializerMethodField('calculate_total_price')

    def calculate_total_items(self, order:Order):
        return sum([item.quantity for item in order.orderitems.all()])

    def calculate_total_price(self, order:Order):
        return sum([item.quantity * item.unit_price for item in order.orderitems.all()])


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    # for a time being i m using customer_id field in post form (afterwards grab customer from url authentication headers)
    # customer_id = serializers.IntegerField()

    def validate_cart_id(self, value):
        if not Cart.objects.filter(pk=value).exists():
            raise ValidationError('No cart with the given id was found.')
        return value

    @transaction.atomic()
    def save(self, **kwargs):
        cart_id = self.validated_data['cart_id']
        customer_id = self.context['user'].customer.id
        # order = Order.objects.create(customer_id=self.validated_data['customer_id'])
        order = Order.objects.create(customer_id=customer_id)

        cartitems = CartItem.objects.filter(cart_id=cart_id).all()

        orderitems = [
            OrderItem(
                quantity=item.quantity, 
                unit_price=item.fooditem.unit_price, 
                order=order, 
                fooditem=item.fooditem
            ) 
            for item in cartitems
        ]
        OrderItem.objects.bulk_create(orderitems)
        Cart.objects.filter(pk=cart_id).delete()

        return order


# -- CUSTOMER -- #
class UpdateCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['phone']
        

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'phone']


# -- ADDRESS -- #
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'customer', 'street', 'city', 'state', 'pincode']
    
    customer = serializers.StringRelatedField()

    def create(self, validated_data):
        customer_id = self.context['customer_id']
        return Address.objects.create(customer_id=customer_id, **validated_data)
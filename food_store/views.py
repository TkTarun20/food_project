from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .permissions import IsAdminOrReadOnly
from .pagination import DefaultPagination
from .serializers import AddCartItemSerializer, AddressSerializer, CartItemSerializer, CartSerializer, CategorySerializer, CreateOrderSerializer, CustomerSerializer, FoodImageSerializer, FoodItemSerializer, OrderSerializer, UpdateCartItemSerializer, UpdateCustomerSerializer, UpdateFoodItemSerializer
from .models import CartItem, Category, Customer, FoodImage, FoodItem, Cart, Order, Address
from .filters import FoodItemFilter, OrderFilter
from django.contrib import messages

# Create your views here.

class CategoryViewSet(ModelViewSet):
    # http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    queryset = Category.objects.annotate(fooditems_count=Count('fooditems')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if FoodItem.objects.filter(category_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Category cannot be deleted because it includes one or more food items.'}, status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class FoodItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category', 'type', 'unit_price']
    filterset_class = FoodItemFilter
    pagination_class = DefaultPagination
    queryset = FoodItem.objects.select_related('category').prefetch_related('images').order_by('pk').all()
    ordering_fields = ['unit_price', 'category__title']
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateFoodItemSerializer
        return FoodItemSerializer


class FoodImageViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'head', 'options']
    serializer_class = FoodImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        fooditem_id = self.kwargs['fooditem_pk']
        return FoodImage.objects.filter(food_item_id=fooditem_id).all()
    
    def get_serializer_context(self):
        return {'fooditem_id': self.kwargs['fooditem_pk']}


class CartViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'head', 'options']
    queryset = Cart.objects.prefetch_related('cartitems__fooditem').all()
    serializer_class = CartSerializer
    pagination_class = DefaultPagination
    # permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     if self.request.method in ['POST', 'DELETE']:
    #         return [AllowAny()]
    #     return [IsAdminUser()]


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    # permission_classes = [AllowAny]

    def get_queryset(self):
        return CartItem.objects.select_related('fooditem').filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitems__fooditem').all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'placed_at']
    filterset_class = OrderFilter
    pagination_class = DefaultPagination

    def get_permissions(self):
        if self.request.method not in ['PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        customer_id = self.request.user.customer.id
        if self.request.user.is_staff == True:
            return Order.objects.select_related('customer').prefetch_related('orderitems__fooditem').all()
        return Order.objects.filter(customer_id=customer_id).select_related('customer').prefetch_related('orderitems__fooditem')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user': self.request.user}


class CustomerViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method != 'DELETE':
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        customer_id = self.request.user.customer.id
        if self.request.user.is_staff == True:
            return Customer.objects.select_related('user').all()
        return Customer.objects.select_related('user').filter(pk=customer_id)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateCustomerSerializer
        return CustomerSerializer


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.select_related('customer').filter(customer_id=self.kwargs['customer_pk'])

    def get_serializer_context(self):
        return {'customer_id': self.kwargs['customer_pk']}
from django_filters.rest_framework import FilterSet
from .models import FoodItem, Order

class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            'customer': ['exact'],
            'placed_at': ['year', 'month']
        }


class FoodItemFilter(FilterSet):
    class Meta:
        model = FoodItem
        fields = {
            'category': ['exact'],
            'type': ['exact'],
            'unit_price': ['gte', 'lte']
        }
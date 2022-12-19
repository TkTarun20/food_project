from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

from food_store.models import Category, Customer, FoodImage, FoodItem, Order, OrderItem

# Register your models here.

class FoodImageInline(admin.TabularInline):
    model = FoodImage
    extra = 1
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src={instance.image.url} class="thumbnail" />')
        return ''


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    inlines = [FoodImageInline]
    list_display = ['title', 'category_title', 'unit_price', 'type']
    list_select_related = ['category']
    list_editable = ['unit_price']
    list_filter = ['category', 'type']
    prepopulated_fields = {'slug': ['title']}
    autocomplete_fields = ['category']
    search_fields = ['title']

    def category_title(self, fooditem):
        return fooditem.category.title

    class Media:
        css = {
            'all': ['food_store/styles.css']
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'fooditems_count']
    search_fields = ['title']

    @admin.display(ordering='fooditems_count')
    def fooditems_count(self, category):
        url = (
            reverse('admin:food_store_fooditem_changelist')
            + '?'
            + urlencode({
                'category__id': str(category.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, category.fooditems_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(fooditems_count=Count('fooditems'))


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    autocomplete_fields = ['fooditem']
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'payment_status', 'customer']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'orders_count']
    list_select_related = ['user']

    def orders_count(self, customer):
        return customer.orders_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count('orders'))
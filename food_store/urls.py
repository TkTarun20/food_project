from rest_framework_nested import routers
from .views import AddressViewSet, CartItemViewSet, CategoryViewSet, CustomerViewSet, FoodImageViewSet, FoodItemViewSet, CartViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('fooditems', FoodItemViewSet)
router.register('carts', CartViewSet)
router.register('orders', OrderViewSet, basename='orders')
router.register('customers', CustomerViewSet, basename='customers')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('cartitems', CartItemViewSet, basename='cart-cartitems')

images_router = routers.NestedDefaultRouter(router, 'fooditems', lookup='fooditem')
images_router.register('images', FoodImageViewSet, basename='fooditem-images')

addresses_router = routers.NestedDefaultRouter(router, 'customers', lookup='customer')
addresses_router.register('addresses', AddressViewSet, basename='customer-addresses')

urlpatterns = router.urls + carts_router.urls + images_router.urls + addresses_router.urls
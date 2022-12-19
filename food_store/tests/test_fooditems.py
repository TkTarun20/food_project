from http import client
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient
from food_store.models import Category, FoodItem
import pytest

# FIXTURES
@pytest.fixture
def create_fooditem(api_client):
    def do_create_fooditem(fooditem):
        return api_client.post('/food_store/fooditems/', fooditem)
    return do_create_fooditem


# TESTS
# @pytest.mark.skip
@pytest.mark.django_db
class TestCreateFoodItem:

    def test_if_user_is_anonymous_returns_401(self, create_fooditem):
        category = baker.make(Category)
        data = {
            'title': 'a',
            'description': 'a',
            'type': 'V',
            'unit_price': 20,
            'category': category.id
        }
        # client = APIClient()
        # response = api_client.post('/food_store/fooditems/', data=data)

        response = create_fooditem(data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    

    # @pytest.mark.skip
    def test_if_user_is_not_admin_returns_403(self, create_fooditem, user_authentication):
        category = baker.make(Category)
        data = {
            'title': 'a',
            'description': 'a',
            'type': 'V',
            'unit_price': 20,
            'category': category.id
        }
        # client = APIClient()
        # client.force_authenticate(user={})
        # response = api_client.post('/food_store/fooditems/', data=data)
        user_authentication()
        response = create_fooditem(data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
    

    # @pytest.mark.skip
    def test_if_data_is_invalid_returns_400(self, create_fooditem, user_authentication):
        data = {}
        # client = APIClient()
        # client.force_authenticate(user=User(is_staff=True))
        # response = api_client.post('/food_store/fooditems/', data=data)
        user_authentication(is_staff=True)
        response = create_fooditem(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    

    # @pytest.mark.skip
    def test_if_data_is_valid_returns_201(self, create_fooditem, user_authentication):
        category = baker.make(Category)
        data = {
            'title': 'a',
            'description': 'a',
            'type': 'V',
            'unit_price': 20,
            'category': category.id
        }
        # client = APIClient()
        # client.force_authenticate(user=User(is_staff=True))
        # response = api_client.post('/food_store/fooditems/', data=data)
        user_authentication(is_staff=True)
        response = create_fooditem(data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


# @pytest.mark.skip
@pytest.mark.django_db
class TestRetrieveFoodItem:

    def test_if_fooditem_exists_returns_200(self):
        fooditem = baker.make(FoodItem)

        client = APIClient()
        response = client.get(f'/food_store/fooditems/{fooditem.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': fooditem.id,
            'title': fooditem.title,
            'description': fooditem.description,
            'type': fooditem.type,
            'unit_price': fooditem.unit_price,
            'category': fooditem.category.id,
            'images': []
        }
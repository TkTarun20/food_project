from django.contrib.auth.models import User
from food_store.models import Category
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient
import pytest


# FIXTURES (specific to this module)
@pytest.fixture
def create_category(api_client):
    def do_create_category(category):
        return api_client.post('/food_store/categories/', category)
    return do_create_category


# @pytest.mark.skip
@pytest.mark.django_db
class TestCreateCategory:
    
    # @pytest.mark.skip
    # @pytest.mark.django_db
    def test_if_user_is_anonymous_returns_401(self, create_category):
        # client = APIClient()
        # response = api_client.post('/food_store/categories/', {'title': 'a'})
        
        response = create_category({'title': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    

    # @pytest.mark.skip
    def test_if_user_is_not_admin_returns_403(self, create_category, user_authentication):
        # client = APIClient()
        # client.force_authenticate(user={})
        # response = api_client.post('/food_store/categories/', {'title': 'a'})
        
        user_authentication()
        response = create_category({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
    # @pytest.mark.skip
    def test_if_data_is_invalid_returns_400(self, create_category, user_authentication):
        # client = APIClient()
        # client.force_authenticate(user=User(is_staff=True))
        # response = api_client.post('/food_store/categories/', {'title': ''})
        
        user_authentication(is_staff=True)
        response = create_category({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    

    # @pytest.mark.skip
    def test_if_data_is_valid_returns_201(self, create_category, user_authentication):
        # client = APIClient()
        # client.force_authenticate(user=User(is_staff=True))
        # response = api_client.post('/food_store/categories/', {'title': 'a'})
        
        user_authentication(is_staff=True)
        response = create_category({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


# @pytest.mark.skip
@pytest.mark.django_db
class TestRetrieveCategory:

    def test_if_category_exists_returns_200(self, api_client):
        category = baker.make(Category)
        
        # client = APIClient()
        response = api_client.get(f'/food_store/categories/{category.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': category.id,
            'title': category.title,
            'fooditems_count': 0
        }

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from todo.models import Todo

User = get_user_model()


@pytest.fixture
def get_client():
    client = APIClient()
    return client


@pytest.fixture
def get_user():
    user = User.objects.create_user(email="test@example.com", password="testtesttest")
    return user


@pytest.fixture
def get_todo(get_user):
    todo = Todo.objects.create(user=get_user, title="testtitle")
    return todo


@pytest.mark.django_db
class TestTodoList:
    def test_get_todo_response_200_status(self, get_client, get_user):
        url = reverse("todo-list")
        user = get_user
        get_client.force_authenticate(user=user)
        response = get_client.get(url)
        assert response.status_code == 200

    def test_create_todo_response_201_status(self, get_client, get_user):
        url = reverse("todo-list")
        user = get_user
        get_client.force_authenticate(user=user) 
        data = {"title": "reading books"}
        response = get_client.post(url, data)
        assert response.status_code == 201

    def test_create_todo_response_401_status(self, get_client, get_user):
        url = reverse("todo-list")
        # user = get_user
        # get_client.force_authenticate(user = user)
        data = {"title": "reading books"}
        response = get_client.post(url, data)
        assert response.status_code == 401

    def test_create_todo_response_400_status(self, get_client, get_user):
        url = reverse("todo-list")
        user = get_user
        get_client.force_authenticate(user=user)
        data = {
            # "title" : "reading books"
        }
        response = get_client.post(url, data)
        assert response.status_code == 400

    def test_delete_todo_response_200_status(self, get_client, get_user, get_todo):
        url = reverse("todo-detail", kwargs={"pk": 1})
        user = get_user
        get_client.force_authenticate(user=user)
        todo = get_todo
        response = get_client.delete(url)
        assert response.status_code == 204


# and other tests...

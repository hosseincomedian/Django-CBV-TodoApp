from django.urls import path, include
from .views import (
    TodoListView,
    TodoCreateView,
    TodoCompleteView,
    TodoUpdateView,
    TodoDeleteView,
)


urlpatterns = [
    path("", TodoListView.as_view(), name="todo-list"),
    path("create/", TodoCreateView.as_view(), name="todo-create"),
    path("complete/", TodoCompleteView.as_view(), name="todo-complete"),
    path("update/<int:pk>/", TodoUpdateView.as_view(), name="todo-update"),
    path("delete/<int:pk>/", TodoDeleteView.as_view(), name="todo-delete"),
    path("api/v1/", include("todo.api.v1.urls")),
]

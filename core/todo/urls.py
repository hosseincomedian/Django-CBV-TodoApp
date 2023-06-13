

from django.urls import path, include
from .views import TodoListView, TodoCreateView, TodoCompleteView
urlpatterns = [
    path('', TodoListView.as_view(), name='todo-list'),
    path('create/', TodoCreateView.as_view(), name='todo-create'),
    path('complete/', TodoCompleteView.as_view(), name='todo-complete'),
]

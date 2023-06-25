from rest_framework.viewsets import ModelViewSet
from todo.models import Todo
from .serializers import TodoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .paginations import DefaultPagination
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTodoUser


class TodoModelViewSet(ModelViewSet):
    permission_classes = (
        IsAuthenticated,
        IsTodoUser,
    )
    model = Todo
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("user", "complete")
    search_fields = ("title",)
    pagination_class = DefaultPagination

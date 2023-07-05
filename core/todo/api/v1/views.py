from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .permissions import IsTodoUser
from todo.models import Todo
from .serializers import TodoSerializer
from .paginations import DefaultPagination

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


class ClimaticConditionAPIGenericView(GenericAPIView):
    @method_decorator(cache_page(60 * 20))
    def get(self, request, *args, **kwargs):
        api_key = "12f1f12d8aaa3b198eb979110ce828ea"
        city = "Esfahan"
        url =  f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}"
        response = requests.get(url).json()
        return Response(response, status=200)
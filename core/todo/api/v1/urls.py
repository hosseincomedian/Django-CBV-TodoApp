from rest_framework import routers
from django.urls import path
from .views import TodoModelViewSet, ClimaticConditionAPIGenericView

router = routers.DefaultRouter()
router.register("todo", TodoModelViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('climatic-condition', ClimaticConditionAPIGenericView.as_view(), name='climatic-condition')
]
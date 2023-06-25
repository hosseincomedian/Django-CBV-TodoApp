from rest_framework import routers
from .views import TodoModelViewSet

router = routers.DefaultRouter()
router.register("todo", TodoModelViewSet)

urlpatterns = router.urls

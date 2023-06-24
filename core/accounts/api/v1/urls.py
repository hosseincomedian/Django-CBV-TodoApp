from django.urls import path
from accounts.api.v1 import views
urlpatterns = [

    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    path('activation/confirm/<str:token>/', views.ActivationApiView.as_view(), name='activation-confirm'),

    path('test/', views.test.as_view()),
]

from django.urls import path
from accounts.api.v1 import views
from rest_framework_simplejwt.views import (TokenVerifyView, TokenRefreshView)

urlpatterns = [

    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    path('activation/confirm/<str:token>/', views.ActivationApiView.as_view(), name='activation-confirm'),
    path('activation/resend/', views.ActivationResendApiView.as_view(), name='activation-resend'),

    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password'),

    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.TokenLogoutApiView.as_view(), name='token-logout'),

    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),

]

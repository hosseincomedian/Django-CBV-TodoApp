from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from . import serializers
from rest_framework import status
from mail_templated import EmailMessage
from accounts.api.utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

User = get_user_model()

class test(APIView):

    def get(self, request, *args, **kwargs):
        return Response('test')
    
class RegistrationApiView(generics.GenericAPIView): 
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data = {
                "email" : serializer.validated_data.get('email') 
            }
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, "ho@gmail.com", to=[email])
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_200_OK) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class ActivationApiView(generics.GenericAPIView):    
    def get(self, request, token):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError :
            return Response({'details':'token is expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.InvalidSignatureError :
            return Response({'details':'token is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        user_id = token.get('user_id')
        user_obj = get_object_or_404(User, pk=user_id)
        if user_obj.is_verified :
            return Response({'details':'user is already verified'}, status=status.HTTP_400_BAD_REQUEST)
        user_obj.is_verified = True
        user_obj.save()
        return Response(token, status=status.HTTP_200_OK)

class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = serializers.ActivationResendSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email = serializer.validated_data['email'])
        if user.is_verified:
            return Response({'details':'user is already verified'}, status=status.HTTP_400_BAD_REQUEST)
        token = self.get_token(user)
        email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, "ho@gmail.com", to=[user.email])
        EmailThread(email_obj).start()
        return Response({"details": "email sent"}, status=status.HTTP_200_OK) 
        
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
class ChangePasswordApiView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'details': 'Password updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = serializers.CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class TokenLogoutApiView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({ 'details' : 'User Logged out successfully'}, status = status.HTTP_200_OK) 
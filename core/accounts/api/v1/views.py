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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from . import serializers
from rest_framework import status

class test(APIView):

    def get(self, request, *args, **kwargs):
        return Response('test')
    
class RegistrationApiView(generics.GenericAPIView): 
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "email" : serializer.validated_data.get('email') 
            }
            return Response(data, status=status.HTTP_200_OK) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

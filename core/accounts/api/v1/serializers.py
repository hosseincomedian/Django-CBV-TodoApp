from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password1')

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        try:
            validate_password(attrs.get('password'))
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('password1', None)
        return User.objects.create_user(**validated_data)
    
class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError({"details": "email does not exist"})
        return super().validate(attrs)
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password1'):
            raise serializers.ValidationError({"details": "new password is not equal to old new password1"})
        try:
            validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return super().validate(attrs)
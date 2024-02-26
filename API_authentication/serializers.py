from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
# from django.contrib.auth.models import User
from django.conf import settings
from API_authentication.models import User

# User = settings.AUTH_USER_MODEL

UserModel = get_user_model()    
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'is_verified']
        extra_kwargs = {
            'password': {'write_only':True}
        }
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password != password2:
            raise serializers.ValidationError("Password and confirm password does not match.")
        
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
class UserAccountVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp   = serializers.CharField()
        
     
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)
    class Meta:
        model = User
        fields = ['email', 'password']

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']
    
from user import models, utils
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user"""

    class Meta:
        model = models.User
        fields = ('id', 'name', 'login', 'password', 'user_type', 'phone', 'status')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        # read_only_fields = ('user_type', )

    def create(self, validated_data):
        """Create user with encrypted password and return it"""
        user = models.User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_type'] = user.user_type
        # ...

        return token
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from .models import User


User = get_user_model()


class EmailTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class UserSerializer(serializers.ModelSerializer):

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError(
                _('Password must have at least 8 characters'))
        return password

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True,
                                     'style': {'input_type': 'password'}}}

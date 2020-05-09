from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer, UserSerializer

User = get_user_model()


class EmailTokenObtainPairView(TokenObtainPairView):

    def to_internal_value(self, data):
        try:
            try:
                email = data['email']
                return User.objects.get(email=email)
            except KeyError:
                raise serializers.ValidationError(_('email is required field'))
            except ValueError:
                raise serializers.ValidationError(_('wrong email format'))
        except User.DoesNotExist:
            raise serializers.ValidationError(_('Object does not exist'))
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):

    @action(detail=False, methods=['post'])
    def register(self, request, **kwargs):
        validated_data = request.data
        print(validated_data)
        serializer = UserSerializer(data=validated_data)
        print(serializer.get_validators())
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            user = User.objects.create(
                email=validated_data['email']
            )
            user.set_password(validated_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

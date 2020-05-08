from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path(r'api/auth/refresh',
         TokenRefreshView.as_view(), name='token_refresh'),
    path(r'api/auth/login', views.EmailTokenObtainPairView.as_view(),
         name='token_obtain_pair')
]

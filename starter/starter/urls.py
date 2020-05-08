
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from core.views import EmailTokenObtainPairView
from quotes.views import TestView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/quote', TestView.as_view(), name="quote"),
    path('', include('core.urls'))
]

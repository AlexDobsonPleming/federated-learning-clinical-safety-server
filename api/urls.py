from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import FlModelViewSet

router = routers.DefaultRouter()
router.register(r'models', FlModelViewSet)

urlpatterns = [
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls)),
]

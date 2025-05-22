# api/urls.py (or your project’s root urls.py)
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_nested import routers
from .views import FlModelViewSet, LocalModelViewSet

router = routers.DefaultRouter()
router.register(r'models', FlModelViewSet)

nested = routers.NestedDefaultRouter(router, r'models', lookup='model')
nested.register(r'locals', LocalModelViewSet, basename='model-locals')

urlpatterns = [
    path("auth/token/", obtain_auth_token, name="api-token-auth"),

    path("", include(router.urls)),
    path("", include(nested.urls)),
]

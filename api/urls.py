from django.urls import include, path
from rest_framework_nested import routers
from .views import FlModelViewSet, LocalModelViewSet

router = routers.DefaultRouter()
router.register(r'models', FlModelViewSet)

# create a nested router for /models/{model_pk}/…
nested = routers.NestedDefaultRouter(router, r'models', lookup='model')
nested.register(r'locals', LocalModelViewSet, basename='model-locals')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested.urls)),
]

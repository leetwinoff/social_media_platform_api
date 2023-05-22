from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, PostViewSet

router = DefaultRouter()
router.register("profile", ProfileViewSet)
router.register("post", PostViewSet)

urlpatterns = [
    # Other URL patterns
    path("", include(router.urls)),
    path("", include(router.urls)),
]

app_name = "profile_services"

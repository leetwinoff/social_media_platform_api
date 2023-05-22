from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet


router = DefaultRouter()
router.register("profile", ProfileViewSet)

urlpatterns = [
    # Other URL patterns
    path("profile/", include(router.urls)),
]

app_name = "profile_services"

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from profile_services.views import (
    ProfileViewSet,
    PostViewSet,
    TagViewSet,
    # CommentViewSet,
)

router = DefaultRouter()
router.register("profile", ProfileViewSet)
router.register("post", PostViewSet)
router.register("tag", TagViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "profile_services"

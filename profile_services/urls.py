from django.urls import include, path
from rest_framework.routers import DefaultRouter
from profile_services.views import (
    ProfileViewSet,
    PostViewSet,
    LikeViewSet,
    CommentViewSet,
)

router = DefaultRouter()
router.register("profile", ProfileViewSet)
router.register("post", PostViewSet)
router.register("like", LikeViewSet)
router.register("comment", CommentViewSet)

urlpatterns = [
    # Other URL patterns
    path("", include(router.urls)),
]

app_name = "profile_services"

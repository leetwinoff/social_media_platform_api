from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from profile_services.models import Profile, Post
from profile_services.serializers import (
    ProfileSerializer,
    ProfileListSerializer,
    PostSerializer,
    PostListSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in (
            "create",
            "update",
            "partial_update",
            "destroy",
        ):
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        return ProfileSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

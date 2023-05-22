from rest_framework import viewsets

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

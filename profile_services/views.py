from rest_framework import viewsets, generics, status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from profile_services.models import Profile, Post, Like
from profile_services.permissions import IsAdminOrIfAuthenticatedReadOnly
from profile_services.serializers import (
    ProfileSerializer,
    ProfileListSerializer,
    PostSerializer,
    PostListSerializer,
    LikeSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

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
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer


class LikeViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin
):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post doesn't exist"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        like = serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"error": "You are not authorized to delete this like"},
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

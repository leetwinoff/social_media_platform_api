from rest_framework import viewsets, status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import F
from rest_framework.viewsets import GenericViewSet

from profile_services.models import Profile, Post, Like, Comment, Tag
from profile_services.permissions import IsAdminOrIfAuthenticatedReadOnly
from profile_services.serializers import (
    ProfileSerializer,
    ProfileListSerializer,
    PostSerializer,
    PostListSerializer,
    LikeSerializer,
    CommentSerializer,
    ProfileDetailSerializer,
    ProfileDetailUpdateSerializer,
    PostDetailSerializer,
    FollowUnfollowSerializer,
    TagSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrIfAuthenticatedReadOnly)

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        elif self.action == "retrieve":
            if self.get_object().user == self.request.user:
                return ProfileDetailUpdateSerializer
            return ProfileDetailSerializer
        elif self.action in ["follow", "unfollow"]:
            return FollowUnfollowSerializer
        return ProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            username = self.request.query_params.get("username")
            if username:
                queryset = queryset.filter(user__username__icontains=username)
        return queryset.distinct()

    def perform_create(self, serializer):
        user = self.request.user

        profile = serializer.save(user=user)

        posts = Post.objects.filter(user=user)
        posts.update(profile=profile)

        profile.posts_count = F("posts_count") + posts.count()
        profile.save()

    def get_permissions(self):
        if self.action in ["create", "list", "follow", "unfollow"]:
            return []
        return super().get_permissions()

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        profile = self.get_object()
        user = request.user

        if profile.user == user:
            return Response(
                {"detail": "You cannot follow your own profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile.followers.add(user)
        profile.save()

        user_profile = user.profile
        user_profile.following.add(profile.user)
        user_profile.save()

        profile_serializer = self.get_serializer(profile)
        user_profile_serializer = ProfileDetailSerializer(user_profile)
        return Response(
            {
                "profile": profile_serializer.data,
                "user_profile": user_profile_serializer.data,
            }
        )

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk=None):
        profile = self.get_object()
        user = request.user

        profile.followers.remove(user)
        profile.save()

        user_profile = user.profile
        user_profile.following.remove(profile.user)
        user_profile.save()

        profile_serializer = self.get_serializer(profile)
        user_profile_serializer = ProfileDetailSerializer(user_profile)
        return Response(
            {
                "profile": profile_serializer.data,
                "user_profile": user_profile_serializer.data,
            }
        )


class TagViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrIfAuthenticatedReadOnly)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related("tags")
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrIfAuthenticatedReadOnly)

    def get_queryset(self):
        tags = self.request.query_params.get("tags")

        queryset = self.queryset

        if tags:
            queryset = queryset.filter(tags__name__icontains=tags)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        elif self.action == "retrieve":
            post = self.get_object()
            if post.user == self.request.user:
                return PostSerializer
            else:
                return PostDetailSerializer

        elif self.action == "add_comment":
            return CommentSerializer

        elif self.action in ["add_like", "remove_like"]:
            return LikeSerializer

        elif self.action == "add_tag":
            return TagSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)
        profile = Profile.objects.get(user=self.request.user)
        profile.posts.add(post)

    @action(detail=True, methods=["post"])
    def add_like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if post.likes.filter(user=user).exists():
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like = Like.objects.create(user=user, post=post)
        post.likes.add(like)

        return Response({"detail": "You liked this post"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def remove_like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        try:
            like = post.likes.get(user=user)
            like.delete()

            return Response(
                {"detail": "You unlike this post"}, status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        user = request.user

        comment_content = request.data.get("content", "")
        comment = Comment.objects.create(user=user, post=post, content=comment_content)
        post.comments.add(comment)
        return Response(
            {"detail": "You leave a comment on this post"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def add_tag(self, request, pk=None):
        post = self.get_object()

        tag_name = request.data.get("name", "")
        tag = Tag.objects.create(post=post, name=tag_name)

        post.tags.add(tag)
        return Response({"detail": "Tag added to the post"}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ["create", "list", "add_like", "remove_like"]:
            return []
        return super().get_permissions()

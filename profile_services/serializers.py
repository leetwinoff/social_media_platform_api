from rest_framework import serializers

from profile_services.models import Profile, Post, Like, Comment, Tag
from user.serializers import UserSerializer


class UsernameField(serializers.RelatedField):
    def to_representation(self, value):
        return value.username


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "profile_picture",
            "bio",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = self.context["request"].user
        if Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError("A profile already exists for this user.")
        validated_data["user"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user

        # if instance.user != user:
        #     raise serializers.ValidationError(
        #         "You are not allowed to update this profile."
        #     )
        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance


class ProfileListSerializer(serializers.ModelSerializer):
    user = UsernameField(read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "user", "profile_picture", "bio")


class CommentSerializer(serializers.ModelSerializer):
    user = UsernameField(read_only=True)

    class Meta:
        model = Comment
        fields = ["user", "content"]
        read_only_fields = ["id"]


class LikeSerializer(serializers.ModelSerializer):
    user = UsernameField(read_only=True)

    class Meta:
        model = Like
        fields = ("user",)


class LikeRepresentationMixin:
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        likes = instance.likes.all()

        if likes.count() >= 2:
            representation["likes"] = f"{likes[0]} and {likes.count() - 1} other users"
        else:
            representation["likes"] = LikeSerializer(likes, many=True).data

        return representation


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)

    def to_representation(self, instance):
        return instance.name


class PostSerializer(LikeRepresentationMixin, serializers.ModelSerializer):
    user = UsernameField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "post_image",
            "post_description",
            "created_at",
            "comments",
            "tags",
            "likes",
        )
        read_only_fields = (
            "created_at",
            "likes",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        profile = user.profile
        validated_data["user"] = user
        validated_data["profile_id"] = profile.id
        post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        user_serializer = self.fields["user"]
        user_instance = instance.user

        user_serializer.update(user_instance, user_data)

        instance.post_image = validated_data.get("post_image", instance.post_image)
        instance.post_description = validated_data.get(
            "post_description", instance.post_description
        )
        instance.created_at = validated_data.get("created_at", instance.created_at)

        tags_data = validated_data.pop("tags", None)
        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_data["name"])
                instance.tags.add(tag)

        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()


class PostDetailSerializer(LikeRepresentationMixin, serializers.ModelSerializer):
    user = UsernameField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "post_image",
            "post_description",
            "tags",
            "likes",
            "comments",
        )
        read_only_fields = (
            "created_at",
            "likes",
        )


class PostListSerializer(LikeRepresentationMixin, serializers.ModelSerializer):
    user = UsernameField(read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "post_image",
            "post_description",
            "tags",
            "likes",
            "created_at",
        )
        read_only_fields = ("created_at",)


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    posts = PostSerializer(many=True, read_only=True)
    followers = UserSerializer(many=True, read_only=True)
    following = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "profile_picture",
            "bio",
            "posts",
            "followers",
            "following",
        )


class ProfileDetailUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    followers = UserSerializer(many=True, read_only=True)
    following = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "profile_picture",
            "bio",
            "posts",
            "followers",
            "following",
        )
        read_only_fields = ("id", "user", "posts")

    def update(self, instance, validated_data):
        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance


class FollowUnfollowSerializer(serializers.Serializer):
    pass

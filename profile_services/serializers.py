from rest_framework import serializers

from profile_services.models import Profile, Post, Like, Comment
from user.models import User
from user.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "user", "profile_picture", "bio")
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = self.context["request"].user
        if Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError("A profile already exists for this user.")
        validated_data["user"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user

        if instance.user != user:
            raise serializers.ValidationError(
                "You are not allowed to update this profile."
            )
        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance


class ProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ("id", "user", "profile_picture", "bio")


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        post = self.context["post"]
        comment = Comment.objects.create(user=user, post=post, **validated_data)
        return comment


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ("user", "post_image", "post_description", "created_at", "comments")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)
        post = Post.objects.create(user=user, **validated_data)
        return post

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = self.fields["user"]
        user_instance = instance.user

        user_serializer.update(user_instance, user_data)

        instance.post_image = validated_data.get("post_image", instance.post_image)
        instance.post_description = validated_data.get(
            "post_description", instance.post_description
        )
        instance.created_at = validated_data.get("created_at", instance.created_at)

        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()


class PostListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ("user", "post_image", "post_description", "created_at")


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Like
        fields = "__all__"


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "profile_picture",
            "bio",
            "posts",
        )
        read_only_fields = ("user.email",)

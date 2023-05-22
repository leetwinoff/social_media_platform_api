from rest_framework import serializers

from profile_services.models import Profile, Post
from user.models import User
from user.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ("id", "user", "profile_picture", "bio")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = self.fields["user"]
        user_instance = instance.user

        user_serializer.update(user_instance, user_data)

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


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ("user", "post_image", "post_description", "created_at")

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
    user = UserSerializer(many=True)

    class Meta:
        model = Post
        fields = ("user", "post_image", "post_description", "created_at")

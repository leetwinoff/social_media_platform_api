import os.path
import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def profile_image_file_path(instance, filename):
    _, extension = os.path.splitext(
        filename,
    )
    filename = f"{instance.user.username}-{uuid.uuid4()}.{extension}"
    return os.path.join("profile_pictures/", filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=profile_image_file_path, null=True, blank=True
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(
        filename,
    )
    filename = f"{instance.user.username}-{uuid.uuid4()}.{extension}"
    return os.path.join("post_images/", filename)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to=post_image_file_path)
    post_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} was created at {self.created_at}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.id}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

from django.contrib import admin
from profile_services.models import Profile, Like, Post, Comment

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)

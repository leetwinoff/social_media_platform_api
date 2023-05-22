from rest_framework import viewsets

from profile_services.models import Profile
from profile_services.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

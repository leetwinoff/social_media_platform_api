from rest_framework import viewsets

from profile_services.models import Profile
from profile_services.serializers import ProfileSerializer, ProfileListSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        return ProfileSerializer

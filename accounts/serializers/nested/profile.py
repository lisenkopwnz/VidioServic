from rest_framework import serializers
from accounts.models.profile import Profile


class ProfileShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'description',
            'user_photo',
            'country',
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'description',
            'user_photo',
            'country',
        )

from rest_framework.exceptions import ParseError
from django.contrib.auth import get_user_model
from djnago.contrib.auth.password.passwod_validation import validate_password
from rest_framework import serializers


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'second_name',
            'email',
            'password',
        )

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                'Email is already registered'
            )
        return email

    def validate_password(self, value):
        validate_password(value)
        return (value)

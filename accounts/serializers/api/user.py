from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password

User = get_user_model()
# region ------------------- AUTHENTICATION AND AVTORITHATION -------------------


class RegistrationSerializer(RegisterSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'telephone',
            'password',

        )

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exist():
            raise serializers.ValidationError('Пользователь с такой почтой уже зарегистрирован.')
        return email

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# endregion ---------------------------------------------------------------------

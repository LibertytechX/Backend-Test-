import re
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class CreateUserSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password1",
            "password2",
        )

    def validate_password1(self, password1):
        """Validate user's inputed password on signup

        Args:
            password1 (str): user's password

        Raises:
            serializers.ValidationError: raise password requirements

        Returns:
            str: returns the validated password
        """
        # Regex pattern to match at least one digit, one uppercase letter,
        # one lowercase letter, one special character, and length >= 8
        regex_pattern = (
            r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )
        if not re.match(regex_pattern, password1):
            raise serializers.ValidationError(
                "Password must contain at least one digit, "
                "one uppercase letter, one lowercase letter, "
                "one special character, and length >= 8"
            )
        return password1

    def validate(self, data):
        """Validate user's inputed data on signup"""
        errors = {}
        email = data.get("email")
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")
        if User.objects.filter(email__iexact=email):
            errors["error"] = _("The email address is already in use")
            raise serializers.ValidationError(errors)
        if User.objects.filter(username__iexact=username):
            errors["error"] = _("Username is taken!")
            raise serializers.ValidationError(errors)
        if password1 != password2:
            errors["error"] = _("The two password fields didn't match.")
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        """Create a new user with the given validated data"""
        email = validated_data.get("email")
        password = validated_data.get("password1")
        username = validated_data.get("username")
        user = User.objects.create_user(
            email=email, username=username, password=password
        )
        return user


class LoginSerializer(ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(label="Username", required=False)
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        username = attrs.get("username")
        if email:
            user = User.objects.filter(email__iexact=email).first()
            if user and user.check_password(password):
                attrs["user"] = user
                return attrs
            else:
                raise serializers.ValidationError({"error": "Invalid credentials"})
        else:
            user = User.objects.filter(username__iexact=username).first()
            if user and user.check_password(password):
                attrs["user"] = user
                return attrs
            else:
                raise serializers.ValidationError({"error": "Invalid credentials"})

    class Meta:
        model = User
        fields = ("email", "username", "password")

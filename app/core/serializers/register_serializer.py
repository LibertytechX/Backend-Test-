from rest_framework import serializers

from core.models import User
from django.contrib.auth.password_validation import validate_password


# Create your serializer(s) here.
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password],
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }

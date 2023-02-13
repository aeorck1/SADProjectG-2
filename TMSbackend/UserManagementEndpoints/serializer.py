from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializers for the user model"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'department', )
        extra_kwargs = {
            'password' : {
                'write_only': True,
                'min_length': 5
            },
        }

    def create(self, validated_data):
        """Creating user from validated data"""

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update user"""

        password = validated_data.pop('password', None)

        user = super().update(instance, validated_data)

        if password is not None:
            user.set_password(password)
            user.save()

        return user

class ManagerSerializer(UserSerializer):
    """Serializers for the user model"""

    def create(self, validated_data):
        """Creating user from validated data"""

        return get_user_model().objects.create_manager(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user Authentication Token"""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'passowrd'},
        trim_whitespace=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            self.context.get('request'), username=email, password=password
        )

        if not user:
            msg = _('Unable to authenticate with the provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
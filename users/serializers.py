from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Roles


class RoleSerializer (serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ('id_role', 'name')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email','first_name', 'last_name','date_of_birth',
                  'password', 'password_confirm')

    def validate(self, attrs):
        password = attrs.get('password', '')
        password_confirm = attrs.get('password_confirm', '')

        if password != password_confirm:
            raise serializers.ValidationError("Las contaseñas no coinciden.")


        id = User.objects.filter(id=attrs.get('id')).exists()
        email = User.objects.filter(email=attrs.get('email')).exists()

        return attrs

    def create(self, validated_data):
        role = Roles.objects.get(name="Cliente")
        user = User.objects.create_user(
            id=validated_data['id'],
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth=validated_data['date_of_birth'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=role
        )
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    id = serializers.CharField(read_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=80, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'id', 'password', 'full_name', 'access_token', 'refresh_token', 'role']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Las credenciales son invalidas")
        user_tokens = user.tokens()

        print()

        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh')),
            'role': user.role.name
        }

class LogoutUserSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')

        return attrs

    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')



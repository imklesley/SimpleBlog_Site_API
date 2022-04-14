from django.contrib.auth import authenticate
from rest_framework import serializers

from ..models import Account


class RegisterAccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, allow_null=False, style={'input_type': 'password'})

    class Meta:
        model = Account
        fields = ('full_name', 'cpf', 'email', 'username', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        account = Account(
            full_name=self.validated_data['full_name'],
            cpf=self.validated_data['cpf'],
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        account.set_password(password)
        account.save()

        return account


class LoginAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=False, allow_blank=False)
    password = serializers.CharField(write_only=True, allow_null=False, allow_blank=False,
                                     style={'input_style': "password"})

    def get_user(self):
        email = self.validated_data['email']
        password = self.validated_data['password']

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({'detail': 'Email or password are invalid'})
        return user

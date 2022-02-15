from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.hashers import make_password
from .models import User, Match


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User

    def validate_password(self, value: str) -> str:
        return make_password(value)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'gender',
            'avatar',
        )
        model = User


class MatchSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Match
        fields = ('user',)

    validators = [
        UniqueTogetherValidator(
            queryset=Match.objects.all(),
            fields=['user', 'liked_user'],
            message='Вы уже отправили лайк'
        )
    ]

    def validate(self, data):
        if data['user'] == data['liked_user']:
            raise serializers.ValidationError(
                'Нельзя лайкать самого себя'
            )
        return data

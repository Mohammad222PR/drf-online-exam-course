from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from account.choices import USER_ROLE_STUDENT, USER_ROLE_INSTRUCTOR


class UserCreateSerializer(BaseUserCreateSerializer):
    role = serializers.ChoiceField(
        choices=(
            (USER_ROLE_INSTRUCTOR, "مربی"),
            (USER_ROLE_STUDENT, "دانش اموز"),
        )
    )

    class Meta(BaseUserCreateSerializer.Meta):
        fields = BaseUserCreateSerializer.Meta.fields + ("role",)

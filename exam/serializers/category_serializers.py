from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import (
    Category,
    FavoriteCategory,
)

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "created",
        ]


class FavoriteCategoryListRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title")

    class Meta:
        model = FavoriteCategory
        fields = [
            "id",
            "category",
        ]


class FavoriteCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCategory
        fields = [
            "category",
        ]

    def create(self, validated_data):

        return FavoriteCategory.objects.create(
            **validated_data,
            student_id=self.context["user_id"],
        )

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

    def validate(self, attrs):
        category_id = attrs["category"]
        student_id = self.context["user_id"]

        favorite_category_exists = FavoriteCategory.objects.filter(
            category_id=category_id, student_id=student_id
        ).exists()

        if favorite_category_exists:
            raise serializers.ValidationError(
                "شما قبلا این دسته بندی رو به دسته بندی های مورد علاقتون اضافه کردید"
            )

        return super().validate(attrs)

    def create(self, validated_data):

        return FavoriteCategory.objects.create(
            **validated_data,
            student_id=self.context["user_id"],
        )

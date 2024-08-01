from rest_framework import viewsets, mixins
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
)
from authentication.permissions import IsStudent
from ..serializers import category_serializers
from ..models import Category, FavoriteCategory


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = category_serializers.CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]


class FavoriteCategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated, IsStudent]

    def get_serializer_class(self):
        if self.action == "create":
            return category_serializers.FavoriteCategoryCreateSerializer
        return category_serializers.FavoriteCategoryListRetrieveSerializer

    def get_queryset(self):
        return (
            FavoriteCategory.objects.select_related("category")
            .filter(student_id=self.request.user.id)
            .all()
        )

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

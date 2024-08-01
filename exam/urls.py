from rest_framework.routers import DefaultRouter
from .views import category_views,exam_views
urlpatterns = []

router = DefaultRouter()

############# Main routers #############
router.register(r"categories", category_views.CategoryViewSet, basename="categories")

router.register(
    r"favorite-categories",
    category_views.FavoriteCategoryViewSet,
    basename="favorite-categories",
)

router.register(r"exams", exam_views.ExamViewSet, basename="exams")

urlpatterns += router.urls


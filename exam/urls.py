from rest_framework.routers import DefaultRouter
from .views import (
    answer_views,
    category_views,
    exam_views,
    questions_views,
    score_views,
)
from rest_framework_nested import routers

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

router.register(r"questions", questions_views.QuestionViewSet, basename="questions")

router.register(r"scores", score_views.ScoreViewSet, basename="scores")

router.register(r"my-scores", score_views.MyScoreViewSet, basename="my-scores")


############# Nested routers #############
exam_router = routers.NestedSimpleRouter(router, r"exams", lookup="exam")

exam_router.register(
    r"questions", questions_views.ExamQuestionViewSet, basename="questions"
)

exam_router.register(r"answers", answer_views.AnswerViewSet, basename="answers")

exam_router.register(r"scores", score_views.ExamScoreViewSet, basename="exam-scores")


urlpatterns += router.urls

urlpatterns += exam_router.urls

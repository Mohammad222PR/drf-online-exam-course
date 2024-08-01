from rest_framework import viewsets, mixins
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAdminUser,
)
from authentication.permissions import (
    IsInstructor,
    IsInstructorExamOwner,
)
from ..serializers import questions_serializers
from ..models import Question


class QuestionViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = Question.objects.all()

        if self.request.method in SAFE_METHODS:
            queryset = queryset.select_related("exam")

        if self.action == "retrieve":
            queryset = queryset.prefetch_related("options")

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return questions_serializers.AdminQuestionRetrieveSerializer

        return questions_serializers.AdminQuestionListSerializer


class ExamQuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsInstructor, IsInstructorExamOwner]

    def get_queryset(self):
        queryset = Question.objects.all()

        if self.request.method in SAFE_METHODS:
            queryset = (
                queryset.filter(
                    exam_id=self.kwargs["exam_pk"],
                    exam__instructor_id=self.request.user.id,
                )
                .select_related("exam")
                .all()
            )

        if self.action == "retrieve":
            queryset = queryset.prefetch_related("options")

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return questions_serializers.QuestionRetrieveSerializer

        if self.request.method not in SAFE_METHODS:
            return questions_serializers.QuestionCreateUpdateSerializers

        return questions_serializers.QuestionListSerializer

    def get_serializer_context(self):
        return {"exam_id": self.kwargs["exam_pk"]}

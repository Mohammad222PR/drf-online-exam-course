from rest_framework import viewsets, mixins
from ..models import Answer
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from authentication.permissions import (
    IsInstructor,
)
from ..serializers import answer_serializers


class AnswerViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated, IsInstructor]
    serializer_class = answer_serializers.AnswerListRetrieveSerializer

    def get_queryset(self):
        return Answer.objects.filter(
            question__exam_id=self.kwargs["exam_pk"],
            question__exam__instructor_id=self.request.user.id,
        ).select_related("student", "question", "selected_option")

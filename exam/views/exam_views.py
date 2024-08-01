from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, AllowAny
from ..serializers import exam_serializers
from authentication.permissions import IsInstructor, IsInstructorOwner, IsStudent
from ..models import Exam, Participation, Question, Answer, Score

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related("instructor", "category").all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]


        return [IsAuthenticated(), IsInstructor(), IsInstructorOwner()]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return exam_serializers.ExamRetrieveSerializer

        if self.request.method not in SAFE_METHODS:
            return exam_serializers.ExamCreateUpdateSerializer

        return exam_serializers.ExamListSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, AllowAny
from ..serializers import exam_serializers, questions_serializers
from authentication.permissions import IsInstructor, IsInstructorOwner, IsStudent
from ..models import Exam, Participation, Question, Answer, Score

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related("instructor", "category").all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]

        if self.action == "next_question":
            return [IsAuthenticated(), IsStudent()]

        return [IsAuthenticated(), IsInstructor(), IsInstructorOwner()]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return exam_serializers.ExamRetrieveSerializer

        if self.request.method not in SAFE_METHODS:
            return exam_serializers.ExamCreateUpdateSerializer

        return exam_serializers.ExamListSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    @action(detail=True, methods=["GET"])
    def next_question(self, request: Request, pk):
        user_id = request.user.id

        exam = get_object_or_404(Exam, pk=pk)

        participation, created = Participation.objects.get_or_create(
            student_id=user_id,
            exam_id=pk,
            defaults={"expires_at": timezone.now() + exam.duration},
        )

        if not created and timezone.now() >= participation.expires_at:
            return Response(
                {"detail": "زمان آزمون به پایان رسیده است"},
                status=status.HTTP_403_FORBIDDEN,
            )

        next_question = (
            Question.objects.filter(exam_id=pk)
            .exclude(answers__student=user_id)
            .first()
        )

        if not next_question:
            return Response(
                {"detail": "شما به تمامی سوالات پاسخ داده اید"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = questions_serializers.StudentQuestionRetrieveSerializer(
            next_question
        )

        return Response(serializer.data)


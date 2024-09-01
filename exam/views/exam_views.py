from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q, FilteredRelation, F
from rest_framework import status
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, AllowAny
from ..serializers import exam_serializers, questions_serializers, score_serializers
from ..serializers import (
    exam_serializers,
    questions_serializers,
    score_serializers,
    answer_serializers,
)
from authentication.permissions import IsInstructor, IsInstructorOwner, IsStudent
from .. import choices
from ..models import Exam, Participation, Question, Answer, Score


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related("instructor", "category").all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]

        if self.action in ["next_question", "finish", "reply"]:
            return [IsAuthenticated(), IsStudent()]

        return [IsAuthenticated(), IsInstructor(), IsInstructorOwner()]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return exam_serializers.ExamRetrieveSerializer

        if self.action == "finish":
            return score_serializers.ScoreSerializer

        if self.action == "reply":
            return answer_serializers.AnswerCreateSerializer

        if self.request.method not in SAFE_METHODS:
            return exam_serializers.ExamCreateUpdateSerializer

        return exam_serializers.ExamListSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_throttles(self):
        if self.action == "reply":
            self.throttle_scope = "reply"
        if self.action == "next_question":
            self.throttle_scope = "next_question"
        if self.action == "finish":
            self.throttle_scope = "finish"
        return super().get_throttles()

    @action(detail=True, methods=["GET"])
    def next_question(self, request: Request, pk):
        user_id = request.user.id

        exam = get_object_or_404(Exam, pk=pk)

        participation, created = Participation.objects.get_or_create(
            student_id=user_id,
            exam_id=pk,
            defaults={"expires_at": timezone.now() + exam.duration},
        )

        if (
            not created
            and Score.objects.filter(exam_id=exam, student_id=user_id).exists()
        ):
            return Response(
                {"detail": "شما قبلا دراین ازمون شرکت کرده اید"},
                status=status.HTTP_403_FORBIDDEN,
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

    @action(detail=True, methods=["POST"])
    def finish(self, request: Request, pk):
        student_id = request.user.id

        participation = Participation.objects.filter(
            student_id=student_id, exam_id=pk
        ).exists()

        if not participation:
            return Response(
                {"detail": "شما در این آزمون شرکت نکرده اید"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if Score.objects.filter(student_id=student_id, exam_id=pk).exists():
            return Response(
                {"detail": "نمره شما ثبت شده است و امکان ثبت مجدد وجود ندارد"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        calculated_score = (
            Answer.objects.annotate(
                correct_option=FilteredRelation(
                    "question__options",
                    condition=Q(question__options__is_correct_answer=True),
                )
            )
            .filter(
                student_id=student_id,
                question__exam_id=pk,
                selected_option=F("correct_option"),
            )
            .count()
        )

        total_question = Question.objects.filter(exam_id=pk).count()

        if calculated_score == total_question:
            rank = choices.GOLD
        if calculated_score < total_question:
            rank = choices.SILVER
        if calculated_score < total_question - 5:
            rank = choices.BRONZE
        if calculated_score == 0:
            rank = choices.UNRANKED

        score = Score.objects.create(
            student_id=student_id, exam_id=pk, rank=rank, score=calculated_score
        )

        serializer = score_serializers.ScoreSerializer(score)

        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def favorites(self, request: Request):
        exam = (
            self.get_queryset()
            .filter(category__favorites__student_id=request.user.id)
            .all()
        )

        serializer = self.get_serializer(exam, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def reply(self, request: Request, pk):

        serializer = answer_serializers.AnswerCreateSerializer(
            data=request.data,
            context={"user_id": request.user.id, "exam_id": pk},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

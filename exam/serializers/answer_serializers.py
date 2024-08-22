from datetime import datetime
from rest_framework import serializers
from ..models import Answer, Participation
from account.serializers import RelatedUserSerializer
from .questions_serializers import (
    RelatedQuestionSerializer,
    RelatedQuestionOptionSerializer,
)
from django.utils import timezone


class AnswerListRetrieveSerializer(serializers.ModelSerializer):
    student = RelatedUserSerializer()
    question = RelatedQuestionSerializer()
    selected_option = RelatedQuestionOptionSerializer()

    class Meta:
        model = Answer
        fields = [
            "id",
            "student",
            "question",
            "selected_option",
            "created",
        ]


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            "question",
            "selected_option",
        ]

    def validate(self, attrs):
        question_id = attrs["question"]

        student_id = self.context["user_id"]
        exam_id = self.context["exam_id"]

        participation = Participation.objects.filter(
            student_id=student_id, exam_id=exam_id
        ).first()

        if not participation:
            raise serializers.ValidationError("شما دراین آزمون شرکت نکرده اید")

        if timezone.now() >= participation.expires_at:
            raise serializers.ValidationError("زمان آزمون به اتمام رسیده است")

        answer_exist = Answer.objects.filter(
            student_id=student_id, question_id=question_id
        ).exists()

        if answer_exist:
            raise serializers.ValidationError("شما قبلا به این سوال پاسخ داده اید")

        return super().validate(attrs)

    def create(self, validated_data):

        return Answer.objects.create(
            **validated_data, student_id=self.context["user_id"]
        )

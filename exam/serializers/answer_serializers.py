from datetime import datetime
from rest_framework import serializers
from ..models import Answer, Participation
from account.serializers import RelatedUserSerializer
from .questions_serializers import (
    RelatedQuestionSerializer,
    RelatedQuestionOptionSerializer,
)
from rest_framework.validators import UniqueTogetherValidator


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
        validators = [
            UniqueTogetherValidator(
                queryset=Answer.objects.all(), fields=["student", "question"]
            )
        ]

    def validate(self, attrs):
        # question = attrs.get("question")

        user_id = self.context["user_id"]
        exam_id = self.context["exam_id"]

        exam_student = Participation.objects.filter(
            student_id=user_id, exam_id=exam_id
        ).first()

        # if not exam_student:
        #     raise serializers.ValidationError("شما دراین آزمون شرکت نکرده اید")

        # if Answer.objects.filter(question=question, user_id=user_id).exists():
        #     raise serializers.ValidationError("شما قبلا  به این سوال جواب داده ایده🛑")

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["user_id"] = self.context["user_id"]

        return super().create(validated_data)

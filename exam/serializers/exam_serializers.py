from datetime import datetime
from account.serializers import RelatedUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import (
    Exam,
    Participation,
)


# Global Serializers


class RelatedExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ["id", "title"]


class ExamListSerializer(serializers.ModelSerializer):
    instructor = RelatedUserSerializer()
    category = serializers.CharField(source="category.title")

    class Meta:
        model = Exam
        exclude = ["description"]


class ExamRetrieveSerializer(serializers.ModelSerializer):
    instructor = RelatedUserSerializer()
    category = serializers.CharField(source="category.title")

    class Meta:
        model = Exam
        fields = [
            "id",
            "instructor",
            "title",
            "description",
            "category",
            "duration",
            "created",
        ]


class ExamCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = [
            "title",
            "description",
            "category",
            "duration",
        ]

    def validate_duration(self, duration):
        if duration.total_seconds() < 60:
            raise serializers.ValidationError("مدت ازمون نباید کمتر از 1 دقیقه باشد")
        return duration

    def create(self, validated_data):
        validated_data["instructor_id"] = self.context["user_id"]
        return super().create(**validated_data)


class ParticipationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = [
            "exam",
        ]

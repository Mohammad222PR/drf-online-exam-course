from rest_framework import serializers
from ..models import (
    Result,
)
from .exam_serializers import RelatedExamSerializer
from account.serializers import RelatedUserSerializer


class ResultListRetrieveSerializer(serializers.ModelSerializer):
    student = RelatedUserSerializer()
    exam = RelatedExamSerializer()

    class Meta:
        model = Result
        fields = [
            "student",
            "exam",
            "score",
            "created",
        ]


class StudentResultListRetrieveSerializer(ResultListRetrieveSerializer):
    class Meta(ResultListRetrieveSerializer.Meta):
        exclude = ["student"]

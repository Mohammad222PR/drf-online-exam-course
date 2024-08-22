from rest_framework import serializers
from ..models import Score
from .exam_serializers import RelatedExamSerializer
from account.serializers import RelatedUserSerializer


class ScoreListRetrieveSerializer(serializers.ModelSerializer):
    student = RelatedUserSerializer()
    exam = RelatedExamSerializer()

    class Meta:
        model = Score
        fields = ["student", "exam", "score", "created"]


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = ["score"]
        read_only_fields = ["score"]


class StudentScoreListRetrieveSerializer(ScoreListRetrieveSerializer):
    class Meta(ScoreListRetrieveSerializer.Meta):
        excludes = ["student"]

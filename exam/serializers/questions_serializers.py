from django.db import transaction
from .exam_serializers import RelatedExamSerializer
from rest_framework import serializers
from ..models import (
    Question,
    QuestionOption,
)


# Related Serializers -------------------------------------------------
class RelatedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text"]


class RelatedQuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ["id", "option_text", "is_correct_answer"]


class StudentRelatedQuestionOptionSerializer(RelatedQuestionOptionSerializer):
    class Meta(RelatedQuestionOptionSerializer.Meta):
        exclude = ["is_correct_answer"]


class QuestionListSerializer(serializers.ModelSerializer):
    exam = RelatedExamSerializer()

    class Meta:
        model = Question
        fields = ["id", "exam", "index", "question_text", "created"]


class QuestionRetrieveSerializer(serializers.ModelSerializer):
    exam = RelatedExamSerializer()
    options = RelatedQuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "exam", "index", "question_text", "options", "created"]


class StudentQuestionRetrieveSerializer(QuestionRetrieveSerializer):
    options = StudentRelatedQuestionOptionSerializer(many=True)

    class Meta(QuestionRetrieveSerializer.Meta):
        exclude = ["index", "created", "exam"]


class QuestionOptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ["option_text", "is_correct_answer"]


class QuestionCreateUpdateSerializers(serializers.ModelSerializer):
    options = serializers.ListField(
        child=QuestionOptionListSerializer(), min_length=2, max_length=10
    )

    class Meta:
        model = Question
        fields = ["question_text", "options"]

    def validate_options(self, options):
        correct_options_count = filter(
            lambda option: option.is_correct_answer, options
        ).count()

        if correct_options_count == 0:
            raise serializers.ValidationError(
                "حداقل یک گزینه به عنوان جواب صحیح باید انتخاب شود"
            )

        if correct_options_count > 1:
            raise serializers.ValidationError(
                "یک سوال نمی تواند بیشتر از 1 جواب صحیح داشته باشد"
            )

        return options

    @transaction.atomic()
    def create(self, validated_data):
        exam_id = self.context["exam_id"]
        options = validated_data["options"]
        index = Question.objects.filter(exam_id=exam_id).count() + 1

        question = Question.objects.create(
            exam_id=exam_id,
            index=index,
            question_text=validated_data["question_text"],
        )

        QuestionOption.objects.bulk_create(
            [
                QuestionOption(
                    question=question,
                    option_text=option.option_text,
                    is_correct_answer=option.is_correct_answer,
                )
                for option in options
            ]
        )

        return question

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


class StudentRelatedQuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        exclude = ["is_correct_answer", "created", "question"]


class StudentQuestionRetrieveSerializer(serializers.ModelSerializer):
    options = StudentRelatedQuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "options"]



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


class QuestionRetrieveSerializer(serializers.ModelSerializer):
    options = RelatedQuestionOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "options", "created"]


class QuestionOptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ["option_text", "is_correct_answer"]


class QuestionCreateUpdateSerializers(serializers.ModelSerializer):
    options = QuestionOptionListSerializer(many=True)

    class Meta:
        model = Question
        fields = ["question_text", "options"]

    def validate_options(self, options):
        option_length = len(options)

        if option_length < 2:
            raise serializers.ValidationError(
                "هر سوال حداقل باید شامل 2 گزینه داشته باشد"
            )

        if option_length > 10:
            raise serializers.ValidationError(
                "هر سوال حداکثر باید شامل 10 گزینه داشته باشد"
            )

        correct_options_count = len(
            list(filter(lambda option: option["is_correct_answer"], options))
        )

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

        question = Question.objects.create(
            exam_id=exam_id,
            question_text=validated_data["question_text"],
        )

        QuestionOption.objects.bulk_create(
            [
                QuestionOption(
                    question=question,
                    option_text=option["option_text"],
                    is_correct_answer=option["is_correct_answer"],
                )
                for option in options
            ]
        )

        return question

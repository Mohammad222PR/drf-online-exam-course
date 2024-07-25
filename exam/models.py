from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class FavoriteCategory(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_categories"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="favorites"
    )

    def __str__(self) -> str:
        return self.title


class Exam(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="exams")
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="exams"
    )
    duration = models.DurationField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Participation(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT, related_name="students")
    student = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="students_exams"
    )
    participate_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        unique_together = ["exam", "student"]

    def __str__(self) -> str:
        return self.student.full_name


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    index = models.PositiveSmallIntegerField()
    question_text = models.TextField()
    created = models.DateTimeField()

    def __str__(self) -> str:
        return self.question_text


class QuestionOption(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="options"
    )
    option_text = models.CharField(max_length=500)
    is_correct_answer = models.BooleanField(default=False)
    created = models.DateTimeField()

    def __str__(self) -> str:
        return self.option_text


class Answer(models.Model):
    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name="answers")
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    selected_option = models.ForeignKey(
        QuestionOption, on_delete=models.CASCADE, related_name="answers"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["student", "question"]

    def __str__(self) -> str:
        return self.student.full_name


class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="results")
    score = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.student.full_name

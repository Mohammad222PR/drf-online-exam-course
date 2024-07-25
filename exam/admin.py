from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created")


@admin.register(models.FavoriteCategory)
class FavoriteCategoryAdmin(admin.ModelAdmin):
    list_display = ("student", "category")


@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("instructor", "title", "category", "duration", "created")


@admin.register(models.Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("exam", "student", "participate_at", "expires_at")


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("exam", "index", "question_text", "created")


@admin.register(models.QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ("question", "option_text", "is_correct_answer", "created")


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("student", "question", "selected_option", "created")


@admin.register(models.Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "exam", "score", "created")

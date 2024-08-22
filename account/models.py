from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from . import choices
from .managers import UserManager


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=255)
    role = models.CharField(
        max_length=20,
        choices=choices.USER_ROLE_CHOICES,
        verbose_name="نقش",
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ عضویت")

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "کاربر"
        verbose_name = "کاربران"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def is_staff(self):
        return self.role == choices.USER_ROLE_ADMIN

    @property
    def is_instructor(self):
        return self.role == choices.USER_ROLE_INSTRUCTOR

    @property
    def is_student(self):
        return self.role == choices.USER_ROLE_STUDENT

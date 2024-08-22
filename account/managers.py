from django.contrib.auth.models import BaseUserManager
from .choices import USER_ROLE_ADMIN


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, role):
        if not email:
            raise ValueError("کاربران باید یک ایمیل داشته باشند")

        user = self.model(
            first_name=first_name, last_name=last_name, email=email, role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=USER_ROLE_ADMIN,
            password=password,
        )
        return user

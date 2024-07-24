from django.contrib.auth.models import BaseUserManager
from .choices import USER_ROLE_ADMIN


class UserManager(BaseUserManager):
    def create_user(self, email, password, role):
        if not email:
            raise ValueError("کاربران باید یک ایمیل داشته باشند")

        user = self.model(
            email=email,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password, role=USER_ROLE_ADMIN)
        user.save(using=self._db)
        return user

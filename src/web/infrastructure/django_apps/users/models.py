from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    class Meta:
        db_table = "auth_user"

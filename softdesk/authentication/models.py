from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User model

    Args:
        AbstractUser (_type_): django default user model

    """

    username = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField(verbose_name=("date de naissance"), blank=False)
    can_be_contacted = models.BooleanField(default=True, verbose_name=("contact consent"))
    can_data_be_shared = models.BooleanField(default=True, verbose_name=("share consent"))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=("created time"))

    def __str__(self):
        """
        Returns the string representation of the user.

        """
        return self.username

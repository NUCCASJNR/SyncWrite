#!/usr/bin/env python3

"""User model for the rental app"""

from django.contrib.auth.models import AbstractUser
from sync.models.base_model import BaseModel, models
from django.contrib.auth.hashers import make_password
from typing import Union


def hash_password(password: Union[str, int]) -> str:
    """
    Hashes the password
    @param password: str | int
    @return: The hashed password
    """
    return make_password(password)


class MainUser(AbstractUser, BaseModel):
    """
    The user model
    """

    email = models.EmailField(unique=True, max_length=50, null=False, blank=False)
    username = models.CharField(max_length=50, null=False, blank=False, unique=True)
    password = models.CharField(max_length=150, null=False, blank=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    is_verified = models.BooleanField(default=False)
    reset_code = models.CharField(max_length=6, null=True, blank=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['email', 'username'])
        ]
        db_table = 'users'

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

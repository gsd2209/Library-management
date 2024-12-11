from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)

    # Add related_name to prevent clashes
    groups = models.ManyToManyField(
        Group,
        related_name="library_users",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="library_users",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

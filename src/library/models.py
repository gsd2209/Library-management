from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='library_users',  # Custom related name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='library_users',  # Custom related name
        blank=True,
    )

    class Meta:
        db_table = 'user'

# Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# Borrow Request Model
class BorrowRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')],
        default='pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

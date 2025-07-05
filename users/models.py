from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        admin = 'ADMIN', 'Admin',
        teacher = 'TEACHER', 'Teacher',
        student = 'STUDENT', 'Student',
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.student)

    def __str__(self):
        return f"{self.username} ({self.role})"
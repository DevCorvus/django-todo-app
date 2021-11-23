from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.postgres.functions import RandomUUID
from uuid import uuid4


class User(AbstractUser):
    name = models.CharField(max_length=150, null=True, blank=True)
    uuid = models.UUIDField(primary_key=True, default=uuid4, unique=True, editable=False)
    pass


class Group(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Message(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]

    class Meta:
        ordering = ['-created_at']
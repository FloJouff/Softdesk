from django.db import models
from django.conf import settings
from authentication.models import User
import uuid


class Project(models.Model):
    """Project model"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(
        max_length=50,
        choices=[("back-end", "Back-end"), ("front-end", "Front-end"), ("iOS", "iOS"), ("Android", "Android")],
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_author",
        verbose_name="Project author",
    )
    contributors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, through="Contributor", related_name="Contributors"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    """Contributor model"""
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.contributor.username}"


class Issue(models.Model):
    """Issue model"""

    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    TAG_CHOICES = [
        ("BUG", "Bug"),
        ("FEATURE", "Feature"),
        ("TASK", "Task"),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_issues")
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_issues"
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="TODO")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="LOW")
    tag = models.CharField(max_length=20, choices=TAG_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_comments")
    created_time = models.DateTimeField(auto_now_add=True)

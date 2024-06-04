from django.db import models
from authentication.models import User

import uuid


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(
        max_length=50,
        choices=[("back-end", "Back-end"), ("front-end", "Front-end"), ("iOS", "iOS"), ("Android", "Android")],
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_projects")
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

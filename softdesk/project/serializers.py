from rest_framework import serializers
from authentication.models import User
from project.models import Project, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Project
        fields = ["id", "name", "description", "type", "author", "created_time"]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user", "project"]

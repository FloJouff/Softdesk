from rest_framework import serializers
# from authentication.serializers import UserProjectSerializer
from project.models import Project, Contributor, Issue, Comment
from authentication.models import User


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    contributors = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "type", "author", "contributors", "created_time"]

    def validate(self, data):
        author = data["author"]
        contributors = data.get("contributors", [])

        if author not in contributors:
            contributors.append(author)

        data["contributors"] = contributors
        return data

    def update(self, instance, validated_data):
        # Ne pas écraser les contributeurs existants
        contributors = validated_data.pop("contributors", None)
        instance = super().update(instance, validated_data)

        if contributors is not None:
            for username in contributors:
                user = User.objects.get(username=username)
                if user not in instance.contributors.all():
                    instance.contributors.add(user)

        return instance


class ContributorSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source="project.name")

    class Meta:
        model = Contributor
        fields = ["contributor", "project"]


class IssueSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(slug_field="name", queryset=Project.objects.all())
    assignee = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), allow_null=True)
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Issue
        fields = [
            "id",
            "name",
            "description",
            "author",
            "status",
            "priority",
            "tag",
            "project",
            "assignee",
            "created_time",
        ]

    def create(self, validated_data):
        project = validated_data.pop("project")
        assignee = validated_data.pop("assignee", None)
        issue = Issue.objects.create(project=project, assignee=assignee, **validated_data)
        return issue


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    issue = serializers.SlugRelatedField(slug_field="name", queryset=Issue.objects.all())

    class Meta:
        model = Comment
        fields = ["uuid", "description", "issue", "author", "created_time"]

    def create(self, validated_data):
        issue = validated_data.pop("issue")
        author = validated_data.pop("author")
        comment = Comment.objects.create(issue=issue, author=author, **validated_data)
        return comment

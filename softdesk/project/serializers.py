from rest_framework import serializers
from project.models import Project, Contributor, Issue, Comment
from authentication.models import User


class ContributorSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source="project.name")

    class Meta:
        model = Contributor
        fields = ["contributor", "project"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    issue = serializers.SlugRelatedField(slug_field="name", queryset=Issue.objects.all())

    class Meta:
        model = Comment
        fields = ["uuid", "description", "issue", "author", "created_time"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)


class IssueDetailSerializer(serializers.ModelSerializer):
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


class IssueListSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(slug_field="name", queryset=Project.objects.all())
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Issue
        fields = [
            "id",
            "name",
            "author",
            "project",
            "tag",
        ]

    def create(self, validated_data):
        project = validated_data.pop("project")
        assignee = validated_data.pop("assignee", None)
        issue = Issue.objects.create(project=project, assignee=assignee, **validated_data)
        return issue


class ProjectListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    contributors = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ["id", "name", "type", "author", "contributors"]

    def validate(self, data):
        author = data["author"]
        contributors = list(data.get("contributors", []))

        if author not in contributors:
            contributors.append(author)

        data["contributors"] = contributors
        return data

    def create(self, validated_data):
        contributors = validated_data.pop("contributors")
        project = Project.objects.create(**validated_data)
        project.contributors.set(contributors)
        return project


class ProjectDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    contributors = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), many=True)
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "name", "description", "type", "author", "contributors", "issues", "created_time"]

    def get_issues(self, instance):
        queryset = instance.issues.filter(status="TODO")
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data

    def validate(self, data):
        author = data["author"]
        contributors = list(data.get("contributors", []))

        request = self.context.get("request")
        if request and request.method == "PATCH":
            return data
        author = data.get("author")
        if not author:
            raise serializers.ValidationError({"author": "This field is required."})
        if author not in contributors:
            contributors.append(author)

        data["contributors"] = contributors
        return data

    def update(self, instance, validated_data):
        contributors = validated_data.pop("contributors", None)
        instance = super().update(instance, validated_data)

        if contributors is not None:
            instance.contributors.set(contributors)

        return instance

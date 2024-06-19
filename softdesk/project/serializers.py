from rest_framework import serializers
from project.models import Project, Contributor, Issue, Comment
from authentication.models import User
from authentication.serializers import UserSerializer


class ContributorSerializer(serializers.ModelSerializer):
    """contributor serializer"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = ["id", "user"]

    def create(self, validated_data):
        project = self.context["project"]
        user = validated_data["user"]
        if Contributor.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError("This user is already a contributor of the project.")
        contributor = Contributor(project=project, user=user)
        contributor.save()
        return contributor


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comments"""
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ["uuid", "description", "author", "created_time"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)


class IssueDetailSerializer(serializers.ModelSerializer):
    """Serializer for Issues's detail view"""
    project = serializers.SlugRelatedField(slug_field="name", queryset=Project.objects.all())
    assignee = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), allow_null=True)
    author = serializers.ReadOnlyField(source="author.username")
    comments = serializers.SlugRelatedField(slug_field="uuid", queryset=Comment.objects.all(), many=True)

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
            "comments",
        ]


class IssueCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Create or Update methods of Issues"""
    project = serializers.SlugRelatedField(slug_field="id", queryset=Project.objects.all())
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

    def validate(self, data):
        project = data.get("project")
        assignee = data.get("assignee")

        # if assignee and not project.contributors.filter(contributor=assignee).exists():
        #     raise serializers.ValidationError({"assignee": "The assignee must be a contributor of the project."})
        if assignee and not Contributor.objects.filter(project=project, user=assignee).exists():
            raise serializers.ValidationError({"assignee": "The assignee must be a contributor of the project."})

        return data


class IssueListSerializer(serializers.ModelSerializer):
    """Serializer for List of Issues"""
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Issue
        fields = [
            "id",
            "name",
            "author",
            "tag",
        ]

    def create(self, validated_data):
        project = validated_data.pop("project")
        assignee = validated_data.pop("assignee", None)
        issue = Issue.objects.create(project=project, assignee=assignee, **validated_data)
        return issue


class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer for List of Projects view"""
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Project
        fields = ["id", "name", "description", "author", "type", "contributors"]

    def validate(self, data):
        author = data.get("author", None)

        if not author and self.instance:
            author = self.instance.author

        return data

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        return project

    def validate_name(self, value):
        request = self.context.get("request")
        project_id = self.context.get("view").kwargs.get("pk")

        if Project.objects.filter(name=value).exclude(id=project_id).exists():
            raise serializers.ValidationError("This project already exists")
        return value


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer for Projects's detail view"""
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    contributors = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["id", "name", "description", "type", "author", "contributors", "issues", "created_time"]

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data

    def get_contributors(self, instance):
        return [contributor.username for contributor in instance.contributors.all()]

    def validate(self, data):
        request = self.context.get("request")

        if request and request.method in ["POST", "PUT", "PATCH"]:
            if "author" not in data:
                data["author"] = getattr(self.instance, "author", request.user)

            contributors = list(data.get("contributors", []))
            if data["author"] not in contributors:
                contributors.append(data["author"])
            data["contributors"] = contributors
        return data

    def update(self, instance, validated_data):
        contributors = validated_data.pop("contributors", None)
        instance = super().update(instance, validated_data)

        return instance

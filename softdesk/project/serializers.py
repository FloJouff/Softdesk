from rest_framework import serializers
from project.models import Project, Contributor, Issue, Comment
from authentication.models import User


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ["uuid", "description", "author", "created_time"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = request.user
        return super().create(validated_data)


class IssueDetailSerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        project = data.get("project")
        assignee = data.get("assignee")

        if assignee and not project.contributors.filter(id=assignee.id).exists():
            raise serializers.ValidationError({"assignee": "The assignee must be a contributor of the project."})

        return data


class IssueCreateUpdateSerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        project = data.get("project")
        assignee = data.get("assignee")

        if assignee and not project.contributors.filter(id=assignee.id).exists():
            raise serializers.ValidationError({"assignee": "The assignee must be a contributor of the project."})

        return data


class IssueListSerializer(serializers.ModelSerializer):
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
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    contributors = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "author", "type", "contributors"]

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
    contributors = ContributorSerializer(many=True, read_only=True)
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
            for username in contributors:
                user = User.objects.get(username=username)
                if user not in instance.contributors.all():
                    instance.contributors.add(user)

        return instance

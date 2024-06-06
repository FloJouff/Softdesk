from rest_framework.test import APITestCase
from django.urls import reverse_lazy
from rest_framework import status

from project.models import Project, Issue, Comment
from authentication.models import User


class TestProject(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword", date_of_birth="2005-01-01")
        self.new_user = User.objects.create_user(
            username="newuser", password="newpassword", date_of_birth="2005-02-02"
        )
        self.client.login(username="testuser", password="testpassword")

        self.project = Project.objects.create(
            name="Initial Project",
            description="Initial Description",
            type="back-end",
            author=self.user,
        )
        self.project.contributors.add(self.user)

    def test_create_project(self):
        url = reverse_lazy("projects-list")
        data = {
            "name": "Nouveau Projet",
            "description": "Description du projet",
            "type": "back-end",
            "author": self.user.username,
            "contributors": [self.user.username],
        }
        response = self.client.post(url, data, format="json")

        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)

        # Vérifier que le projet a été créé avec succès
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)
        project = Project.objects.get(name="Nouveau Projet")
        self.assertEqual(project.name, "Nouveau Projet")
        self.assertEqual(project.author, self.user)
        self.assertIn(self.user, project.contributors.all())

    def test_update_project_add_contributor(self):
        url = reverse_lazy("projects-detail", kwargs={"pk": self.project.pk})
        data = {
            "name": self.project.name,
            "description": self.project.description,
            "type": self.project.type,
            "author": self.user.username,
            "contributors": [self.user.username, self.new_user.username],
        }
        response = self.client.put(url, data, format="json")

        if response.status_code != status.HTTP_200_OK:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertIn(self.user, self.project.contributors.all())
        self.assertIn(self.new_user, self.project.contributors.all())

    def test_delete_project(self):
        url = reverse_lazy("projects-detail", kwargs={"pk": self.project.pk})
        response = self.client.delete(url)

        # Imprimer la réponse en cas d'échec pour obtenir plus d'informations
        if response.status_code != status.HTTP_204_NO_CONTENT:
            print(response.data)

        # Vérifier que le projet a été supprimé avec succès
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)


class TestIssue(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass", date_of_birth="2005-02-02")
        self.assignee = User.objects.create_user(
            username="assigneeuser", password="testpass", date_of_birth="2005-02-02"
        )
        self.project = Project.objects.create(name="Test Project", description="Test Description", author=self.user)
        self.client.login(username="testuser", password="testpass")

    def test_create_issue(self):
        url = reverse_lazy("issues-list")
        data = {
            "name": "Test Issue",
            "description": "This is a test issue",
            "status": "TODO",
            "priority": "MEDIUM",
            "tag": "BUG",
            "project": self.project.name,
            "author": self.user.username,
            "assignee": self.user.username,
        }
        response = self.client.post(url, data, format="json")
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Issue.objects.count(), 1)
        self.assertEqual(Issue.objects.get().name, "Test Issue")

    def test_list_issues(self):
        Issue.objects.create(
            name="Test Issue 1",
            description="Test",
            status="TODO",
            priority="MEDIUM",
            tag="BUG",
            project=self.project,
            author=self.user,
            assignee=self.assignee,
        )
        Issue.objects.create(
            name="Test Issue 2",
            description="Test",
            status="TODO",
            priority="HIGH",
            tag="FEATURE",
            project=self.project,
            author=self.user,
            assignee=self.assignee,
        )
        url = reverse_lazy("issues-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Issue.objects.count(), 2)

    def test_update_issue(self):
        issue = Issue.objects.create(
            name="Test Issue",
            description="Test",
            status="TODO",
            priority="MEDIUM",
            tag="BUG",
            project=self.project,
            author=self.user,
            assignee=self.assignee,
        )
        url = reverse_lazy("issues-detail", kwargs={"pk": issue.pk})
        data = {"name": "Updated Issue"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        issue.refresh_from_db()
        self.assertEqual(issue.name, "Updated Issue")

    def test_delete_issue(self):
        issue = Issue.objects.create(
            name="Test Issue",
            description="Test",
            status="TODO",
            priority="MEDIUM",
            tag="BUG",
            project=self.project,
            author=self.user,
            assignee=self.assignee,
        )
        url = reverse_lazy("issues-detail", kwargs={"pk": issue.pk})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Issue.objects.filter(pk=issue.pk).exists())


class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass", date_of_birth="2005-02-02")
        self.project = Project.objects.create(name="Test Project", description="Test Description", author=self.user)
        self.issue = Issue.objects.create(
            name="Test Issue",
            description="Test",
            status="TODO",
            priority="MEDIUM",
            tag="BUG",
            project=self.project,
            author=self.user,
            assignee=self.user,
        )
        self.client.login(username="testuser", password="testpass")

    def test_create_comment(self):
        url = reverse_lazy("comments-list")
        data = {"description": "This is a test comment", "issue": self.issue.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().description, "This is a test comment")

    def test_update_comment(self):
        comment = Comment.objects.create(description="Test Comment", issue=self.issue, author=self.user)
        url = reverse_lazy("comments-detail", kwargs={"pk": comment.pk})
        data = {"description": "Updated Comment"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.description, "Updated Comment")

    def test_delete_comment(self):
        comment = Comment.objects.create(description="Test Comment", issue=self.issue, author=self.user)
        url = reverse_lazy("comments-detail", kwargs={"pk": comment.pk})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

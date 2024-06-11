from rest_framework.test import APITestCase
from django.urls import reverse_lazy
from rest_framework import status

from project.models import Project, Issue, Comment
from authentication.models import User


# class TestProject(APITestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="testpassword", date_of_birth="2005-01-01")
#         self.new_user = User.objects.create_user(
#             username="newuser", password="newpassword", date_of_birth="2005-02-02"
#         )
#         self.client.login(username="testuser", password="testpassword")

#         self.project = Project.objects.create(
#             name="Initial Project",
#             description="Initial Description",
#             type="back-end",
#             author=self.user,
#         )
#         self.project.contributors.add(self.user)

#     def test_create_project(self):
#         url = reverse_lazy("projects-list")
#         data = {
#             "name": "Nouveau Projet",
#             "description": "Description du projet",
#             "type": "back-end",
#             "author": self.user.username,
#             "contributors": [self.user.username],
#         }
#         response = self.client.post(url, data, format="json")

#         if response.status_code != status.HTTP_201_CREATED:
#             print(response.data)

#         # Vérifier que le projet a été créé avec succès
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Project.objects.count(), 2)
#         project = Project.objects.get(name="Nouveau Projet")
#         self.assertEqual(project.name, "Nouveau Projet")
#         self.assertEqual(project.author, self.user)
#         self.assertIn(self.user, project.contributors.all())

#     def test_update_project_add_contributor(self):
#         url = reverse_lazy("projects-detail", kwargs={"pk": self.project.pk})
#         data = {
#             "name": self.project.name,
#             "description": self.project.description,
#             "type": self.project.type,
#             "author": self.user.username,
#             "contributors": [self.user.username, self.new_user.username],
#         }
#         response = self.client.put(url, data, format="json")

#         if response.status_code != status.HTTP_200_OK:
#             print(response.data)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.project.refresh_from_db()
#         self.assertIn(self.user, self.project.contributors.all())
#         self.assertIn(self.new_user, self.project.contributors.all())

#     def test_delete_project(self):
#         url = reverse_lazy("projects-detail", kwargs={"pk": self.project.pk})
#         response = self.client.delete(url)

#         # Imprimer la réponse en cas d'échec pour obtenir plus d'informations
#         if response.status_code != status.HTTP_204_NO_CONTENT:
#             print(response.data)

#         # Vérifier que le projet a été supprimé avec succès
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Project.objects.count(), 0)


# class TestIssue(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="testpass", date_of_birth="2005-02-02")
#         self.assignee = User.objects.create_user(
#             username="assigneeuser", password="testpass", date_of_birth="2005-02-02"
#         )
#         self.other_user = User.objects.create_user(
#             username="otheruser", password="testpass", date_of_birth="2005-02-02"
#         )
#         self.project = Project.objects.create(name="Test Project", description="Test Description", author=self.user)
#         self.project.contributors.add(self.user, self.assignee)
#         self.client.login(username="testuser", password="testpass")

#     def test_create_issue(self):
#         url = reverse_lazy("issues-list")
#         data = {
#             "name": "Test Issue",
#             "description": "This is a test issue",
#             "status": "TODO",
#             "priority": "MEDIUM",
#             "tag": "BUG",
#             "project": self.project.name,
#             "author": self.user.username,
#             "assignee": self.user.username,
#         }
#         response = self.client.post(url, data, format="json")
#         if response.status_code != status.HTTP_201_CREATED:
#             print(response.data)

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Issue.objects.count(), 1)
#         self.assertEqual(Issue.objects.get().name, "Test Issue")

#     def test_create_issue_not_contributor(self):
#         self.client.logout()
#         self.client.login(username="otheruser", password="testpass")
#         url = reverse_lazy("issues-list")
#         data = {
#             "name": "Test Issue",
#             "description": "This is a test issue",
#             "status": "TODO",
#             "priority": "MEDIUM",
#             "tag": "BUG",
#             "project": self.project.name,
#             "author": self.user.username,
#             "assignee": self.user.username,
#         }
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_list_issues(self):
#         Issue.objects.create(
#             name="Test Issue 1",
#             description="Test",
#             status="TODO",
#             priority="MEDIUM",
#             tag="BUG",
#             project=self.project,
#             author=self.user,
#             assignee=self.assignee,
#         )
#         Issue.objects.create(
#             name="Test Issue 2",
#             description="Test",
#             status="TODO",
#             priority="HIGH",
#             tag="FEATURE",
#             project=self.project,
#             author=self.user,
#             assignee=self.assignee,
#         )
#         url = reverse_lazy("issues-list")
#         response = self.client.get(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Issue.objects.count(), 2)

#     def test_update_issue_by_author(self):
#         issue = Issue.objects.create(
#             name="Test Issue",
#             description="Test",
#             status="TODO",
#             priority="MEDIUM",
#             tag="BUG",
#             project=self.project,
#             author=self.user,
#             assignee=self.assignee,
#         )
#         url = reverse_lazy("issues-detail", kwargs={"pk": issue.pk})
#         data = {"name": "Updated Issue"}
#         response = self.client.patch(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         issue.refresh_from_db()
#         self.assertEqual(issue.name, "Updated Issue")

#     def test_update_issue_by_non_author(self):
#         issue = Issue.objects.create(
#             name="Test Issue",
#             description="Test",
#             status="TODO",
#             priority="MEDIUM",
#             tag="BUG",
#             project=self.project,
#             author=self.user,
#             assignee=self.assignee,
#         )
#         self.client.login(username="assigneeuser", password="testpass")
#         url = reverse_lazy("issues-detail", kwargs={"pk": issue.pk})
#         data = {"name": "Updated Issue by Non-Author"}
#         response = self.client.patch(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_delete_issue_by_author(self):
#         issue = Issue.objects.create(
#             name="Test Issue",
#             description="Test",
#             status="TODO",
#             priority="MEDIUM",
#             tag="BUG",
#             project=self.project,
#             author=self.user,
#             assignee=self.assignee,
#         )
#         url = reverse_lazy("issues-detail", kwargs={"pk": issue.pk})
#         response = self.client.delete(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Issue.objects.filter(pk=issue.pk).exists())

#     def test_delete_issue_by_non_author(self):
#         issue = Issue.objects.create(
#             name="Test Issue",
#             description="Test",
#             status="TODO",
#             priority="MEDIUM",
#             tag="BUG",
#             project=self.project,
#             author=self.user,
#             assignee=self.assignee,
#         )
#         self.client.login(username="assigneeuser", password="testpass")
#         url = reverse_lazy("issues-detail", kwargs={"pk": issue.pk})
#         response = self.client.delete(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# class CommentTests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="testpass", date_of_birth="2005-02-02")
#         self.other_user = User.objects.create_user(
#             username="otheruser", password="testpass", date_of_birth="2005-02-02"
#         )
#         self.project = Project.objects.create(name="Test Project", description="Test Description", author=self.user)
#         self.project.contributors.add(self.user, self.other_user)
#         self.issue = Issue.objects.create(
#             name="Test Issue",
#             description="Test",
#             status="TODO",
#             priority="MEDIUM",
#             tag="BUG",
#             project=self.project,
#             author=self.user,
#             assignee=self.user,
#         )
#         self.client.login(username="testuser", password="testpass")

#     def test_create_comment(self):
#         url = reverse_lazy("comments-list")
#         data = {"description": "This is a test comment", "issue": self.issue.name}
#         response = self.client.post(url, data, format="json")
#         if response.status_code != status.HTTP_201_CREATED:
#             print("Response data:", response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Comment.objects.count(), 1)
#         self.assertEqual(Comment.objects.get().description, "This is a test comment")

#     def test_update_comment_by_author(self):
#         comment = Comment.objects.create(description="Test Comment", issue=self.issue, author=self.user)
#         url = reverse_lazy("comments-detail", kwargs={"pk": comment.pk})
#         data = {"description": "Updated Comment"}
#         response = self.client.patch(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         comment.refresh_from_db()
#         self.assertEqual(comment.description, "Updated Comment")

#     def test_update_comment_by_non_author(self):
#         comment = Comment.objects.create(description="Test Comment", issue=self.issue, author=self.user)
#         self.client.login(username="otheruser", password="testpass")
#         url = reverse_lazy("comments-detail", kwargs={"pk": comment.pk})
#         data = {"description": "Updated Comment by Non-Author"}
#         response = self.client.patch(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_delete_comment_by_author(self):
#         comment = Comment.objects.create(description="Test Comment", issue=self.issue, author=self.user)
#         url = reverse_lazy("comments-detail", kwargs={"pk": comment.pk})
#         response = self.client.delete(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

#     def test_delete_comment_by_non_author(self):
#         comment = Comment.objects.create(description="Test Comment", issue=self.issue, author=self.user)
#         self.client.login(username="otheruser", password="testpass")
#         url = reverse_lazy("comments-detail", kwargs={"pk": comment.pk})
#         response = self.client.delete(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_list_comments_visible_to_contributors(self):
#         Comment.objects.create(description="Test Comment 1", issue=self.issue, author=self.user)
#         Comment.objects.create(description="Test Comment 2", issue=self.issue, author=self.user)
#         self.client.login(username="otheruser", password="testpass")
#         url = reverse_lazy("comments-list")
#         response = self.client.get(url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Comment.objects.count(), 2)  # Both comments should be visible


# class ProjectPermissionTests(APITestCase):

#     def setUp(self):
#         self.user1 = User.objects.create_user(username="user1", password="password", date_of_birth="2005-02-02")
#         self.user2 = User.objects.create_user(username="user2", password="password", date_of_birth="2005-02-02")
#         self.user3 = User.objects.create_user(username="user3", password="password", date_of_birth="2005-02-02")
#         self.project = Project.objects.create(name="Test Project", description="A test project", author=self.user1)
#         self.project.contributors.add(self.user1, self.user2)

#     # def get_jwt_token_for_user(self, user):
#     #     from rest_framework_simplejwt.tokens import RefreshToken

#     #     refresh = RefreshToken.for_user(user)
#     #     return str(refresh.access_token)

#     def test_project_read_access_for_contributors(self):
#         self.client.login(username="user2", password="password", date_of_birth="2005-02-02")
#         url = reverse_lazy("projects-detail", args=[self.project.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

#     # def test_project_update_access_for_author(self):
#     #     self.client.login(username="user1", password="password", date_of_birth="2005-02-02")
#     #     url = reverse_lazy("projects-detail", args=[self.project.id])
#     #     response = self.client.patch(url, data={"name": "Updated Project"})
#     #     self.assertEqual(response.status_code, 200)
#     #     self.project.refresh_from_db()
#     #     self.assertEqual(self.project.name, "Updated Project")

#     def test_project_update_access_for_non_author(self):
#         self.client.login(username="user2", password="password", date_of_birth="2005-02-02")
#         url = reverse_lazy("projects-detail", args=[self.project.id])
#         response = self.client.patch(url, data={"name": "Updated Project"})
#         self.assertEqual(response.status_code, 403)

#     def test_project_delete_access_for_author(self):
#         self.client.login(username="user1", password="password", date_of_birth="2005-02-02")
#         url = reverse_lazy("projects-detail", args=[self.project.id])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, 204)

#     def test_project_delete_access_for_non_author(self):
#         self.client.login(username="user2", password="password", date_of_birth="2005-02-02")
#         url = reverse_lazy("projects-detail", args=[self.project.id])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, 403)

#     def test_project_read_access_for_non_contributors(self):
#         self.client.login(username="user3", password="password", date_of_birth="2005-02-02")
#         url = reverse_lazy("projects-detail", args=[self.project.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 403)

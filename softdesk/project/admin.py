from django.contrib import admin

from project.models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):

    list_display = ("name", "type", "author")


class ContributorAdmin(admin.ModelAdmin):

    list_display = ("contributor", "project")


class IssueAdmin(admin.ModelAdmin):

    list_display = ("name", "project", "author")


class CommentAdmin(admin.ModelAdmin):

    list_display = ("description", "issue", "author")


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)

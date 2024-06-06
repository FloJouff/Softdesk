from django.contrib import admin

from project.models import Project, Contributor


class ProjectAdmin(admin.ModelAdmin):

    list_display = ("name", "type", "author")


class ContributorAdmin(admin.ModelAdmin):

    list_display = ("contributor", "project")


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)

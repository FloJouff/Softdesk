from django.contrib import admin

from project.models import Project


class ProjectAdmin(admin.ModelAdmin):

    list_display = ("name", "type", "author")


admin.site.register(Project, ProjectAdmin)

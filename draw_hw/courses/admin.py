from django.contrib import admin
from . import models

class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'class_name', 'instructor']

    search_fields = ['class_name']

    list_filter = []

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'deadline', 'pdf']

    search_fields = ['course']

    list_filter = []

admin.site.register(models.Course, CourseAdmin)

admin.site.register(models.Assignment, AssignmentAdmin)
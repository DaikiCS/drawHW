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

class AnswersAdmin(admin.ModelAdmin):
    list_display = ['hw_name', 'question_no', 'correct_ans', 'assignment']

    search_fields = ['hw_name']

    list_filter = []

admin.site.register(models.Course, CourseAdmin)

admin.site.register(models.Assignment, AssignmentAdmin)

admin.site.register(models.Answers, AnswersAdmin)
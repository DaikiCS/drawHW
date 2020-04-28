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

class AnswerInstructorAdmin(admin.ModelAdmin):
    list_display = ['question_no', 'correct_ans', 'assignment']

    search_fields = ['assignment']

    list_filter = []

class RegisterCourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'student']

    search_fields = ['course']

    list_filter = []

class AnswerStudentAdmin(admin.ModelAdmin):
    list_display = ['question_no', 'correct_ans', 'assignment', 'student']

    search_fields = ['assignment']

    list_filter = []

admin.site.register(models.Course, CourseAdmin)

admin.site.register(models.Assignment, AssignmentAdmin)

admin.site.register(models.AnswerInstructor, AnswerInstructorAdmin)

admin.site.register(models.RegisterCourse, RegisterCourseAdmin)

admin.site.register(models.AnswerStudent, AnswerStudentAdmin)
from courses.models import Course, Assignment
from django import forms

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'class_name', 'instructor', 'description']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'course', 'deadline', 'pdf']
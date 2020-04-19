from courses.models import Course, Assignment, Answer
from django import forms

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'class_name', 'instructor', 'description']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'course', 'deadline', 'pdf']

class AnswersForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question_no', 'correct_ans', 'assignment']
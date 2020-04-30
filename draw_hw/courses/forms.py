from courses.models import Course, Assignment, AnswerInstructor, AnswerStudent
from django import forms

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'class_name', 'instructor', 'description']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'course', 'deadline', 'pdf']


class AnswerInstructorForm(forms.ModelForm):
    class Meta:
        model = AnswerInstructor
        fields = ['question_no', 'correct_ans', 'assignment']

class AnswerStudentForm(forms.ModelForm):
    class Meta:
        model = AnswerStudent
        fields = ['question_no', 'correct_ans', 'assignment', 'student']
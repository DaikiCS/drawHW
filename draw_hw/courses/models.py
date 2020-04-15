from django.db import models

class Course(models.Model):
    code = models.CharField(unique=True, max_length=5)
    class_name = models.CharField(unique=True, max_length=15)
    description = models.CharField(max_length=100)
    instructor  = models.ForeignKey("accounts.User", limit_choices_to={"is_student": False, "is_superuser": False}, on_delete=models.CASCADE, related_name="instructor")

class Assignment(models.Model):
    name = models.CharField(max_length=15)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    pdf = models.FileField(upload_to="pdfs/")

class Answers(models.Model):
    hw_name = models.CharField(max_length=15)
    question_no = models.PositiveSmallIntegerField()
    correct_ans = models.CharField(max_length=1)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
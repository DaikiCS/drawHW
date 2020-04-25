from django.db import models

class Course(models.Model):
    code = models.CharField(unique=True, max_length=5)
    class_name = models.CharField(unique=True, max_length=15)
    description = models.CharField(max_length=100)
    instructor  = models.ForeignKey("accounts.User", limit_choices_to={"is_student": False, "is_superuser": False}, on_delete=models.CASCADE, related_name="instructor")

    def __str__(self):
        return "@{}".format(self.class_name)

class Assignment(models.Model):
    name = models.CharField(max_length=15)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    pdf = models.FileField(upload_to="pdfs/")
    num_q = models.IntegerField(default=0)

    def __str__(self):
        return "@{}".format(self.name)

class AnswerInstructor(models.Model):
    question_no = models.PositiveSmallIntegerField(unique=True)
    correct_ans = models.CharField(max_length=1)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

class RegisterCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey("accounts.User", limit_choices_to={"is_student": True, "is_superuser": False}, on_delete=models.CASCADE, related_name="student")

    class Meta:
        unique_together = (('course', 'student'),)

class AnswerStudent(models.Model):
    question_no = models.PositiveSmallIntegerField(unique=True)
    correct_ans = models.CharField(max_length=1)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey("accounts.User", limit_choices_to={"is_student": True, "is_superuser": False}, on_delete=models.CASCADE, related_name="student_answer")
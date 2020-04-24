from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from courses.models import Course, RegisterCourse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from . import mixins

@login_required()
def register_course(request):
    # deny access for certain users
    if request.user.is_student == False or \
        request.user.is_superuser:
            return HttpResponseForbidden()
    
    error = ''
    # get all registered courses
    courses = []
    rows = RegisterCourse.objects.filter(student=request.user)
    for course in rows:
        courses.append(course.course)

    if request.method == 'POST':
        try:
            # get a course with code
            course = Course.objects.get(code=request.POST.get('courseNumber'))
            # store into registration table
            RegisterCourse.objects.create(course=course, student=request.user)
        except Course.DoesNotExist:
            error = 'Class not found'
        except IntegrityError:
            error = 'You already registered this class'
        except Exception as e:
            error = str(e)

    return render(request, 'student/home.html', {'error': error,
                                                 'courses': courses
                                                })
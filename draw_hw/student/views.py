from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from courses.models import Course, RegisterCourse, Assignment
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from datetime import datetime
from . import mixins

@login_required()
def register_course(request):
    # deny access for certain users
    if request.user.is_student == False or \
        request.user.is_superuser:
            return HttpResponseForbidden()
    
    error = ''
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

    # get all registered courses
    courses = []
    rows = RegisterCourse.objects.filter(student=request.user)
    for course in rows:
        courses.append(course.course)

    return render(request, 'student/home.html', {'error': error,
                                                 'courses': courses
                                                                    })

@login_required()
def course_detail(request, pk):
    # deny access for certain users
    if request.user.is_student == False or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    try: 
        course = Course.objects.get(pk=pk)
        assignments = Assignment.objects.filter(course=course)
    except:
        return HttpResponseRedirect(reverse_lazy('student:student'))

    return render(request, 'student/class.html', {'course': course,
                                                  'assignments': assignments,
                                                  'pk': pk
                                                                            })

def submit_answer(request, pk, pk1):
    # deny access for certain users
    if request.user.is_student == False or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    pass_due = False
    try: 
        course = Course.objects.get(pk=pk)
        assignments = Assignment.objects.filter(course=course)
        assignment = Assignment.objects.get(pk=pk1)

        if assignment.deadline.replace(tzinfo=None) < datetime.today():
            pass_due = True
    except:
        return HttpResponseRedirect(reverse_lazy('student:student'))

    return render(request, 'student/assignment.html', {'course': course,
                                                    'assignments': assignments,
                                                    'assignment': assignment,
                                                    'pk': pk,
                                                    'pk1': pk1,
                                                    'pass_due': pass_due
                                                                            })
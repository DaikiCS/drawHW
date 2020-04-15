from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from courses.forms import CourseForm, AssignmentForm, AnswersForm
from courses.models import Course, Assignment
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

@login_required()
def create_course(request):
    # deny access for certain users
    if request.user.is_student or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    c_form = CourseForm()
    courses = Course.objects.filter(instructor=request.user)

    if request.method == 'POST':
        request.POST = request.POST.copy() # copy post and make it mutable
        c_form = CourseForm(request.POST)
        c_form.data["instructor"] = request.user # save current user

        if c_form.is_valid():
            c_form.save()
            return HttpResponseRedirect(reverse_lazy('instructor:instructor'))
    return render(request, 'instructor/home.html', {'c_form': c_form, 
                                                    'courses': courses})
@login_required()
def course_detail(request, pk):
    # deny access for certain users
    if request.user.is_student or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    courses = Course.objects.filter(instructor=request.user)
    courses = courses.filter(pk=pk)
    for course in courses:
        assignments = Assignment.objects.filter(course=course)
    c_form = False

    for course in courses:
        c_form = CourseForm(instance=course) # pass current data

    if request.method == 'POST':
        request.POST = request.POST.copy() # copy post and make it mutable
        c_form = CourseForm(request.POST, instance=course) # pass user data
        c_form.data["instructor"] = request.user # save current user
        c_form.data["code"] = course.code # save current course

        if c_form.is_valid():
            c_form.save()
            return redirect('instructor:course_detail', pk=pk)
    return render(request, 'instructor/class.html', {'pk': pk,
                                                     'c_form': c_form, 
                                                     'courses': courses,
                                                     'assignments': assignments
                                                                            })

@login_required()
def create_assignment(request, pk):
    # deny access for certain users
    if request.user.is_student or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    courses = Course.objects.filter(instructor=request.user)
    courses = courses.filter(pk=pk)
    for course in courses:
        assignments = Assignment.objects.filter(course=course)
    a_form = AssignmentForm()

    if request.method == 'POST':
        request.POST = request.POST.copy() # copy post and make it mutable
        a_form = AssignmentForm(request.POST, request.FILES)
        for course in courses:
            a_form.data["course"] = course # save current course
        # save deadline
        time = a_form.data["duedate"] + ' ' + a_form.data["duetime"]
        a_form.data["deadline"] = datetime.strptime(time, "%Y-%m-%d %H:%M")

        if a_form.is_valid():
            a_form.save()
            return redirect('instructor:assignment', pk=pk)

    return render(request, 'instructor/assignment.html', {'pk': pk,
                                                          'a_form': a_form,
                                                          'courses': courses,
                                                          'assignments': assignments
                                                                            })


@login_required()
def add_answers(request, pk, pk1):
    # deny access for certain users
    if request.user.is_student or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    courses = Course.objects.filter(instructor=request.user)
    courses = courses.filter(pk=pk)
    for course in courses:
        assignments = Assignment.objects.filter(course=course)
        assignments = assignments.filter(pk=pk1)
    an_form = AnswersForm()

    if request.method == 'POST':
        request.POST = request.POST.copy() # copy post and make it mutable
        an_form = AnswersForm(request.POST)
        for course in courses:
            an_form.data["course"] = course # save current course

        an_form.data["hw_name"] = assignments
        print(assignments)
        count = an_form.data["questionCount"]
        print(count)

        if an_form.is_valid():
            an_form.save()
            return redirect('instructor:assignment', pk=pk, pk1=pk1)

    return render(request, 'instructor/addAnswer.html', {'pk': pk,
                                                          'pk1': pk1,  
                                                          'an_form': an_form,
                                                          'courses': courses,
                                                          'assignments': assignments
                                                                            })

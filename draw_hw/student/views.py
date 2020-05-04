from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from courses.models import Course, RegisterCourse, Assignment, AnswerStudent, AnswerInstructor
from courses.forms import AnswerStudentForm
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

    exist_lst = []
    name_lst = []
    course = RegisterCourse.objects.get(course__pk=pk, student=request.user)
    assignments = Assignment.objects.filter(course=course.course)
    answer_exist = AnswerStudent.objects.filter(student=request.user)

    for answer in answer_exist:
        name = str(answer.assignment)
        name = (name.replace(name[:1], ''))
        exist_lst.append(name)

    for assignment in assignments:
        for i in range(len(exist_lst)):
            if exist_lst[i] == assignment.name:
                name = str(assignment.name)
                name_lst.append(name)
                break
    
    try: 
        course = RegisterCourse.objects.get(course__pk=pk, student=request.user)
        assignments = Assignment.objects.filter(course=course.course)
    except Exception as e:
        print(e) 
        return HttpResponseRedirect(reverse_lazy('student:student'))

    return render(request, 'student/class.html', {'course': course.course,
                                                  'assignments': assignments,
                                                  'pk': pk,
                                                  'name_lst': name_lst
                                                                            })

#
#   will need to implement error handling when adding answers more than one
#
def submit_answer(request, pk, pk1):
    # deny access for certain users
    if request.user.is_student == False or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    exist_lst = []
    name_lst = []
    course = RegisterCourse.objects.get(course__pk=pk, student=request.user)
    assignments = Assignment.objects.filter(course=course.course)
    answer_exist = AnswerStudent.objects.filter(student=request.user)

    for answer in answer_exist:
        name = str(answer.assignment)
        name = (name.replace(name[:1], ''))
        exist_lst.append(name)

    for assignment in assignments:
        for i in range(len(exist_lst)):
            if exist_lst[i] == assignment.name:
                name = str(assignment.name)
                name_lst.append(name)
                break


    answerKey = True
    past_due = False
    an_form = AnswerStudentForm()

    try: 
        course = RegisterCourse.objects.get(course__pk=pk, student=request.user)
        assignments = Assignment.objects.filter(course=course.course)
        assignment = Assignment.objects.get(pk=pk1)
        answer_instructor_exist = AnswerInstructor.objects.filter(assignment=assignment)
        
        if len(answer_instructor_exist) == 0:
            answerKey = False

        if assignment.deadline.replace(tzinfo=None) < datetime.today():
            past_due = True
    except:
        return HttpResponseRedirect(reverse_lazy('student:student'))

    count = assignment.num_q
    if request.method == 'POST':
        request.POST = request.POST.copy() # copy post and make it mutable
        an_form = AnswerStudentForm(request.POST)

        an_form.data["course"] = course 
        an_form.data["assignment"] = assignment
        an_form.data["student"] = request.user

        if "questionCount" in request.POST:
            count = an_form.data["questionCount"]  

        # save each answer 1 at a time
        for i in range(1, count+1):
            an_form.data["correct_ans"] = an_form.data["q"+str(i)]
            an_form.data["question_no"] = i   

            answer = AnswerStudent(
                question_no=an_form.data["question_no"], 
                correct_ans=an_form.data["correct_ans"], 
                assignment=an_form.data["assignment"],
                student=an_form.data["student"]
            )

            if an_form.is_valid():
                answer.save()       

    return render(request, 'student/assignment.html', {'course': course.course,
                                                    'assignments': assignments,
                                                    'assignment': assignment,
                                                    'num_q': assignment.num_q,
                                                    'pk': pk,
                                                    'pk1': pk1,
                                                    'past_due': past_due,
                                                    'answerKey': answerKey,
                                                    'name_lst': name_lst
                                                                            })

def get_grade(request, pk):
    # deny access for certain users
    if request.user.is_student == False or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    scores = []
    correct_lst = []
    total = []
    hws = []
    try: 
        # get a course
        course = Course.objects.get(pk=pk)
        # get all the assignments
        assignments = Assignment.objects.filter(course=course)

        passed = True

        # loop each assignment
        for assignment in assignments:
            score = 0
            correct = 0
            count = assignment.num_q

            # get answer for each assignment with user
            answer_student = AnswerStudent.objects.filter(assignment=assignment, student=request.user)
            answer_instructor = AnswerInstructor.objects.filter(assignment=assignment)

            if assignment.deadline.replace(tzinfo=None) >= datetime.today():
                passed = False
                # submitted on time
                if answer_instructor and answer_student:
                    for s, i in zip(answer_student, answer_instructor):
                        if s.correct_ans == i.correct_ans:
                            correct += 1

                    score = correct / count * 100

                    hws.append(assignment)
                    scores.append(round(score, 2))
                    total.append(count)
                    correct_lst.append(correct)
            else: # pass due date
                # submitted on time
                if answer_instructor and answer_student:
                    for s, i in zip(answer_student, answer_instructor):
                        if s.correct_ans == i.correct_ans:
                            correct += 1

                    score = correct / count * 100

                    hws.append(assignment)
                    scores.append(round(score, 2))
                    total.append(count)
                    correct_lst.append(correct)
                # did not submit on time
                elif answer_instructor:
                    hws.append(assignment)
                    scores.append(round(score, 2))
                    total.append(count)
                    correct_lst.append(0)
            
        assignments = zip(hws, correct_lst, total, scores)
    except Exception as ex:
        print(ex)
        return HttpResponseRedirect(reverse_lazy('student:student'))

    return render(request, 'student/gradeStudent.html', {'pk': pk,
                                                         'course': course,
                                                         'assignments': assignments,
                                                         'passed': passed
                                                        })
                                                                            
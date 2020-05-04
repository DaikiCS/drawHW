from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from courses.forms import CourseForm, AssignmentForm, AnswerInstructorForm
from courses.models import Course, Assignment, AnswerInstructor, AnswerStudent, RegisterCourse
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

    try:
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
    except Exception as ex:
        print(ex)
        return HttpResponseRedirect(reverse_lazy('instructor:instructor'))


@login_required()
def create_assignment(request, pk):
    # deny access for certain users
    if request.user.is_student or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    try:
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
    except Exception as ex:
        print(ex)
        return HttpResponseRedirect(reverse_lazy('instructor:instructor')) 


@login_required()
def assignment_detail(request, pk, pk1):
    # deny access for certain users
    if request.user.is_student or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    courses = Course.objects.filter(instructor=request.user)
    courses = courses.filter(pk=pk)
    eh_form = AssignmentForm()
   
    try:
        for course in courses:
            assignments = Assignment.objects.filter(course=course)
            assignments = assignments.filter(pk=pk1)
        
        for assignment in assignments:
            dt = str(assignment.deadline.replace(tzinfo=None))
            date = (dt.split(' ')[0])
            time = (dt.split(' ')[1])
            time1 = (time.split(':')[0])
            time2 = (time.split(':')[1])
            time = time1 + ":" + time2
            eh_form = AssignmentForm(instance=assignment)


        if request.method == 'POST':
            request.POST = request.POST.copy() # copy post and make it mutable
            eh_form = AssignmentForm(request.POST, request.FILES, instance=assignment)

            for course in courses:
                eh_form.data["course"] = course # save current course

            # save deadline
            time = eh_form.data["duedate"] + ' ' + eh_form.data["duetime"]
            eh_form.data["deadline"] = datetime.strptime(time, "%Y-%m-%d %H:%M")
            

            if eh_form.is_valid():
                eh_form.save()
                return redirect('instructor:edit_homework', pk=pk, pk1=pk1)

        return render(request, 'instructor/edithw.html', {'pk': pk,
                                                            'pk1': pk1,  
                                                            'eh_form': eh_form,
                                                            'courses': courses,
                                                            'assignments': assignments,
                                                            'date': date,
                                                            'time': time
                                                                            })
    except Exception as ex:
        print(ex)
        return HttpResponseRedirect(reverse_lazy('instructor:instructor'))


#
#   will need to implement error handling when adding answers more than one
#
@login_required()
def add_answers(request, pk, pk1):
    # deny access for certain users
    if request.user.is_student or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    try: 
        courses = Course.objects.filter(instructor=request.user)
        courses = courses.filter(pk=pk)

        for course in courses:
            assignments = Assignment.objects.filter(course=course)
            assignments = assignments.filter(pk=pk1)

        an_form = AnswerInstructorForm()

        if request.method == 'POST':
            request.POST = request.POST.copy() # copy post and make it mutable
            an_form = AnswerInstructorForm(request.POST)

            for course in courses:
                an_form.data["course"] = course # save current course

            for assignment in assignments:
                an_form.data["assignment"] = assignment

            if "questionCount" in request.POST:
                count = an_form.data["questionCount"]  
            
            count = int(count)
            # save each answer 1 at a time
            for i in range(1, count+1):
                an_form.data["correct_ans"] = an_form.data["q"+str(i)]
                an_form.data["question_no"] = i   

                answer = AnswerInstructor(
                    question_no=an_form.data["question_no"], 
                    correct_ans=an_form.data["correct_ans"], 
                    assignment=an_form.data["assignment"]
                )

                if an_form.is_valid():
                    answer.save()            
        
            if an_form.is_valid():
                for assignment in assignments:
                    assignment.num_q = count
                    assignment.save()
                return redirect('instructor:course_detail', pk=pk)

        return render(request, 'instructor/addAnswer.html', {'pk': pk,
                                                            'pk1': pk1,  
                                                            'an_form': an_form,
                                                            'courses': courses,
                                                            'assignments': assignments
                                                                            })
    except Exception as ex:
        print(ex)
        return HttpResponseRedirect(reverse_lazy('instructor:instructor'))

@login_required()
def grades(request, pk):
    # deny access for certain users
    if request.user.is_student or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    try: 
        courses = Course.objects.filter(instructor=request.user)
        courses = courses.filter(pk=pk)
        for course in courses:
            assignments = Assignment.objects.filter(course=course)
        click_on_course = False
                
        return render(request, 'instructor/gradeInstructor.html', {'pk': pk,
                                                        'click_on_course': click_on_course, 
                                                        'courses': courses,
                                                        'assignments': assignments
                                                                            })
    except Exception as ex:
        print(ex)
        return HttpResponseRedirect(reverse_lazy('instructor:instructor'))

@login_required()
def grades_specific(request, pk, pk1):
    # deny access for certain users
    if request.user.is_student or \
        request.user.is_superuser:
            return HttpResponseForbidden()

    
    scores = []
    correct_lst = []
    total = []
    submitted = []
    try:
        # all the courses under this instructor
        courses = Course.objects.filter(instructor=request.user)
        courses = courses.filter(pk=pk)

        # all the asignments under this this courseID
        for course in courses:
            assignments = Assignment.objects.filter(course=course)
            this_homework = assignments.get(pk=pk1)
        click_on_course = True

        # if instructor submitted answers
        answerKey = AnswerInstructor.objects.filter(assignment=this_homework)
        if len(answerKey) == 0:
            answerKey = False

        passed = True
        if this_homework.deadline.replace(tzinfo=None) >= datetime.today():
            passed = False

        # all the students who are registerd in this course
        students = RegisterCourse.objects.filter(course=course)   
        
        # loop each assignment
        for student in students:
            score = 0
            correct = 0
            count = this_homework.num_q
            # get answer for each assignment with user
            answer_student = AnswerStudent.objects.filter(assignment=this_homework, student=student.student)
            answer_instructor = AnswerInstructor.objects.filter(assignment=this_homework)
      
            if len(answer_student) != 0:
                # answered this assignment
                if answer_instructor and answer_student:
                    submitted.append("(submitted)")
                    for s, i in zip(answer_student, answer_instructor):
                        if s.correct_ans == i.correct_ans:
                            correct += 1
                    score = correct / count * 100

                    scores.append(round(score, 2))
                    total.append(count)
                    correct_lst.append(correct)
            else:
                # did not answered this assignment
                submitted.append("(not submitted)")
                scores.append(round(score, 2))
                total.append(count)
                correct_lst.append(0)

        data = zip(students, submitted, correct_lst, total, scores)
    except Exception as ex:
        print(ex)
        return HttpResponseRedirect(reverse_lazy('instructor:instructor'))

    
            
    return render(request, 'instructor/gradeInstructor.html', {'pk': pk,
                                                     'pk1': pk1,
                                                     'click_on_course': click_on_course, 
                                                     'courses': courses,
                                                     'assignments': assignments,
                                                     'this_homework': this_homework,
                                                     'data': data,
                                                     'answerKey': answerKey,
                                                     'passed': passed
                                                                            })

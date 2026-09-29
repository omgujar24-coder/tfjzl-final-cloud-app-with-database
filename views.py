from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.views import generic
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission, Enrollment


# Course List View (Index)
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')[:10]


# Course Detail View
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'


# Enroll in Course View
def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        user = request.user
        if user.is_authenticated:
            Enrollment.objects.get_or_create(user=user, course=course)
            return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))
        else:
            return HttpResponseRedirect(reverse('onlinecourse:login'))


# Submit Exam View
def submit(request, course_id):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    
    # Get user enrollment
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    # Create new Submission instance
    submission = Submission.objects.create(enrollment=enrollment)
    
    # Extract selected choice IDs from request
    selected_choice_ids = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            selected_choice_ids.append(int(value))
    
    # Add selected choices to submission
    choices = Choice.objects.filter(id__in=selected_choice_ids)
    submission.choices.set(choices)
    
    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)


# Show Exam Result View
def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Calculate exam score
    total_score = 0
    grade = 0
    
    selected_choices = submission.choices.all()
    selected_ids = [choice.id for choice in selected_choices]
    
    # Calculate score based on total questions in course lessons
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_score += question.grade
            if question.is_get_score(selected_ids):
                grade += question.grade
                
    score = int((grade / total_score) * 100) if total_score > 0 else 0
    
    context['course'] = course
    context['grade'] = grade
    context['total_score'] = total_score
    context['score'] = score
    context['selected_ids'] = selected_ids
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)


# User Registration View
def registration_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        password = request.POST['password']
        
        try:
            User.objects.get(username=username)
            context['error'] = "Username already exists."
            return render(request, 'onlinecourse/registration.html', context)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            login(request, user)
            return redirect('onlinecourse:index')
            
    return render(request, 'onlinecourse/registration.html', context)


# Login View
def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            return render(request, 'onlinecourse/login.html', {'error': 'Invalid username or password.'})
    return render(request, 'onlinecourse/login.html')


# Logout View
def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')

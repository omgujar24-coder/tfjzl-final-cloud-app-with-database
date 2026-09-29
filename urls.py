from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Route for course list / index view
    path('', views.CourseListView.as_view(), name='index'),

    # Route for user registration, login, and logout
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    # Route for course details
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),

    # Route for course enrollment
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),

    # Route for submitting exam answers
    path('<int:course_id>/submit/', views.submit, name='submit'),

    # Route for showing exam result
    path('<int:course_id>/submission/<int:submission_id>/show_exam_result/', views.show_exam_result, name='show_exam_result'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

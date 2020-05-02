from . import views
from django.urls import path

app_name = 'instructor'

urlpatterns = [
    path('', views.create_course, name='instructor'), 
    path('detail/<slug:pk>/', views.course_detail, name='course_detail'),
    path('detail/<slug:pk>/grades/', views.grades, name='grades'),
    path('detail/<slug:pk>/grades/<slug:pk1>/', views.grades_specific, name='grades_specific'),
    path('detail/<slug:pk>/hw/', views.create_assignment, name='assignment'),
    path('detail/<slug:pk>/hw/edithw/<slug:pk1>/', views.assignment_detail, name='edit_homework'), 
    path('detail/<slug:pk>/hw/edithw/<slug:pk1>/addanswers/', views.add_answers, name='add_answers')
]
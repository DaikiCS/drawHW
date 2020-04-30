from . import views
from django.urls import path

app_name = 'student'

urlpatterns = [
    path('', views.register_course, name='student'),
    path('detail/<slug:pk>/', views.course_detail, name='course_detail'),
    path('detail/<slug:pk>/hw/<slug:pk1>/', views.submit_answer, name='submit_answer'),
    path('detail/<slug:pk>/grade', views.get_grade, name='grade'),
]
from . import views
from django.urls import path

app_name = 'student'

urlpatterns = [
    path('', views.register_course, name='student'),
]
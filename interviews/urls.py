from django.urls import path
from . import views

urlpatterns = [
    path('schedule/<int:job_pk>/<int:user_pk>/', views.schedule_interview, name='schedule_interview'),
    path('list/', views.interview_list, name='interview_list'),
    path('my-interviews/', views.interview_list, name='my_interviews'),
]

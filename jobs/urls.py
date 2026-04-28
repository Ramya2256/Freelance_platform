from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('create/', views.job_create, name='job_create'),
    path('applicants/', views.applicants_list, name='applicants_list'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/applications/', views.job_applications, name='job_applications'),
]

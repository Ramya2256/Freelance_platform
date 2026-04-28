from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_pk>/', views.apply_to_job, name='apply_to_job'),
]

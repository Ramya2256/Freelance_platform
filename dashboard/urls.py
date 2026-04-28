from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('contracts/recruiter/', views.contract_list, name='contract_list_recruiter'),
    path('contracts/freelancer/', views.contract_list, name='contract_list_freelancer'),
    path('earnings/', views.earnings_view, name='earnings'),
]

from django.contrib import admin
from .models import Interview

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('job', 'recruiter', 'freelancer', 'date_time', 'status')
    list_filter = ('status',)

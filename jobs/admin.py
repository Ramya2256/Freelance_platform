from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'category', 'budget', 'deadline', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description', 'required_skills')

from django.contrib import admin
from .models import Assessment

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'job', 'freelancer', 'status', 'score')
    list_filter = ('status',)

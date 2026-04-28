from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'freelancer', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('proposal',)

from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'category', 'job_type', 'experience_level', 
            'description', 'required_skills', 'budget', 'deadline',
            'interview_required', 'assessment_required'
        ]
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe the role, responsibilities, and expectations...'}),
            'required_skills': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, React (comma separated)'}),
        }

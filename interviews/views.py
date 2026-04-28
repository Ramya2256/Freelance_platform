from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Interview
from jobs.models import Job

@login_required
def schedule_interview(request, job_pk, user_pk):
    if request.user.role != 'RECRUITER':
        return redirect('dashboard')
    
    job = get_object_or_404(Job, pk=job_pk, recruiter=request.user)
    freelancer = get_object_or_404(request.user.__class__, pk=user_pk)
    
    if request.method == 'POST':
        date_time = request.POST.get('date_time')
        meeting_link = request.POST.get('meeting_link')
        
        Interview.objects.create(
            job=job,
            recruiter=request.user,
            freelancer=freelancer,
            date_time=date_time,
            meeting_link=meeting_link
        )
        return redirect('interview_list')
        
    return render(request, 'interviews/schedule_form.html', {'job': job, 'freelancer': freelancer})

@login_required
def interview_list(request):
    if request.user.role == 'RECRUITER':
        interviews = request.user.scheduled_interviews.all().order_by('-date_time')
    else:
        interviews = request.user.assigned_interviews.all().order_by('-date_time')
    return render(request, 'interviews/interview_list.html', {'interviews': interviews})

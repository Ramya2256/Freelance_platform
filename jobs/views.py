from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm # Need to create this

def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def job_create(request):
    if request.user.role != 'RECRUITER':
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            # Set status based on button clicked
            if 'save_draft' in request.POST:
                job.status = 'DRAFT'
            else:
                job.status = 'PUBLISHED'
            job.save()
            return redirect('dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def applicants_list(request):
    if request.user.role != 'RECRUITER':
        return redirect('dashboard')
    jobs = request.user.posted_jobs.all()
    return render(request, 'jobs/applicants_list.html', {'jobs': jobs})

@login_required
def my_applications(request):
    if request.user.role != 'FREELANCER':
        return redirect('dashboard')
    applications = request.user.job_applications.all()
    return render(request, 'jobs/my_applications.html', {'applications': applications})

@login_required
def job_applications(request, pk):
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    apps = job.applications.all()
    return render(request, 'jobs/job_applications.html', {'job': job, 'applications': apps})

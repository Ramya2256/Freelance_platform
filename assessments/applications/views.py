from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Application
from jobs.models import Job

@login_required
def apply_to_job(request, job_pk):
    if request.user.role != 'FREELANCER':
        return redirect('dashboard')
    
    job = get_object_or_404(Job, pk=job_pk, is_active=True)
    
    # Check if already applied
    if Application.objects.filter(job=job, freelancer=request.user).exists():
        return redirect('dashboard')
    
    if request.method == 'POST':
        proposal = request.POST.get('proposal')
        budget = request.POST.get('budget')
        portfolio = request.POST.get('portfolio_link')
        
        Application.objects.create(
            job=job,
            freelancer=request.user,
            proposal=proposal,
            proposal_budget=budget,
            portfolio_link=portfolio
        )
        from django.contrib import messages
        messages.success(request, f'Succesfully applied for "{job.title}"!')
        return redirect('dashboard')
        
    return render(request, 'applications/apply_form.html', {'job': job})

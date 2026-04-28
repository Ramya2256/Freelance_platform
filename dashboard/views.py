from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from applications.models import Application
from interviews.models import Interview
from chat.models import Notification

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncDate
import json
from datetime import timedelta
from django.utils import timezone
from dashboard.models import Contract

@login_required
def dashboard_view(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-timestamp')[:5]
    
    if request.user.role == 'RECRUITER':
        # Summary Cards
        posted_jobs = Job.objects.filter(recruiter=request.user)
        total_jobs = posted_jobs.count()
        total_applications = Application.objects.filter(job__recruiter=request.user).count()
        shortlisted = Application.objects.filter(job__recruiter=request.user, status='SHORTLISTED').count()
        hired = Application.objects.filter(job__recruiter=request.user, status='HIRED').count()
        
        # Chart 1: Applications per Job
        jobs_with_counts = posted_jobs.annotate(app_count=Count('applications'))
        chart_apps_per_job = {
            'labels': [j.title for j in jobs_with_counts[:10]],
            'data': [j.app_count for j in jobs_with_counts[:10]]
        }

        # Chart 2: Hiring Trend (Last 6 Months)
        hiring_trend = Application.objects.filter(job__recruiter=request.user, status='HIRED')\
            .annotate(month=TruncMonth('created_at'))\
            .values('month').annotate(count=Count('id')).order_by('month')
        chart_hiring_trend = {
            'labels': [h['month'].strftime('%b %Y') for h in hiring_trend],
            'data': [h['count'] for h in hiring_trend]
        }

        # Chart 3: Job Status Distribution
        open_jobs = posted_jobs.filter(is_active=True).count()
        closed_jobs = posted_jobs.filter(is_active=False).count()
        chart_job_status = {
            'labels': ['Open', 'Closed'],
            'data': [open_jobs, closed_jobs]
        }

        # Chart 4: Applications Over Time (Last 30 Days)
        last_30_days = timezone.now() - timedelta(days=30)
        apps_over_time = Application.objects.filter(job__recruiter=request.user, created_at__gte=last_30_days)\
            .annotate(date=TruncDate('created_at'))\
            .values('date').annotate(count=Count('id')).order_by('date')
        chart_apps_history = {
            'labels': [a['date'].strftime('%d %b') for a in apps_over_time],
            'data': [a['count'] for a in apps_over_time]
        }

        context = {
            'total_jobs': total_jobs,
            'total_applications': total_applications,
            'shortlisted': shortlisted,
            'hired_count': hired,
            'chart_apps_per_job': json.dumps(chart_apps_per_job),
            'chart_hiring_trend': json.dumps(chart_hiring_trend),
            'chart_job_status': json.dumps(chart_job_status),
            'chart_apps_history': json.dumps(chart_apps_history),
            'notifications': notifications
        }
        return render(request, 'dashboard/recruiter_dashboard.html', context)
    else:
        # Summary Cards
        applied_jobs_count = Application.objects.filter(freelancer=request.user).count()
        interview_invites = Interview.objects.filter(freelancer=request.user, status='SCHEDULED').count()
        active_projects = Contract.objects.filter(freelancer=request.user, status='ACTIVE').count()
        earnings = Contract.objects.filter(freelancer=request.user, status='COMPLETED').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        # Chart 1: Applications per Month
        apps_per_month = Application.objects.filter(freelancer=request.user)\
            .annotate(month=TruncMonth('created_at'))\
            .values('month').annotate(count=Count('id')).order_by('month')
        chart_apps_month = {
            'labels': [a['month'].strftime('%b %Y') for a in apps_per_month],
            'data': [a['count'] for a in apps_per_month]
        }

        # Chart 2: Earnings Growth
        earnings_history = Contract.objects.filter(freelancer=request.user, status='COMPLETED')\
            .annotate(month=TruncMonth('end_date'))\
            .values('month').annotate(total=Sum('total_amount')).order_by('month')
        chart_earnings_growth = {
            'labels': [e['month'].strftime('%b %Y') for e in earnings_history],
            'data': [float(e['total']) for e in earnings_history]
        }

        # Chart 3: Project Status
        projects = Contract.objects.filter(freelancer=request.user)
        active = projects.filter(status='ACTIVE').count()
        completed = projects.filter(status='COMPLETED').count()
        cancelled = projects.filter(status='CANCELLED').count()
        chart_project_status = {
            'labels': ['Active', 'Completed', 'Cancelled'],
            'data': [active, completed, cancelled]
        }

        # Chart 4: Work Activity (Apps in last 30 days)
        last_30_days = timezone.now() - timedelta(days=30)
        activity = Application.objects.filter(freelancer=request.user, created_at__gte=last_30_days)\
            .annotate(date=TruncDate('created_at'))\
            .values('date').annotate(count=Count('id')).order_by('date')
        chart_activity_trend = {
            'labels': [a['date'].strftime('%d %b') for a in activity],
            'data': [a['count'] for a in activity]
        }

        context = {
            'applied_jobs_count': applied_jobs_count,
            'interview_invites': interview_invites,
            'active_projects': active_projects,
            'total_earnings': earnings,
            'chart_apps_month': json.dumps(chart_apps_month),
            'chart_earnings_growth': json.dumps(chart_earnings_growth),
            'chart_project_status': json.dumps(chart_project_status),
            'chart_activity_trend': json.dumps(chart_activity_trend),
            'notifications': notifications
        }
        return render(request, 'dashboard/freelancer_dashboard.html', context)

@login_required
def contract_list(request):
    if request.user.role == 'RECRUITER':
        contracts = request.user.contracts_as_recruiter.all()
    else:
        contracts = request.user.contracts_as_freelancer.all()
    return render(request, 'dashboard/contract_list.html', {'contracts': contracts})

@login_required
def earnings_view(request):
    if request.user.role != 'FREELANCER':
        return redirect('dashboard')
    contracts = request.user.contracts_as_freelancer.filter(status='COMPLETED')
    total_earnings = sum(c.total_amount for c in contracts)
    return render(request, 'dashboard/earnings.html', {'contracts': contracts, 'total_earnings': total_earnings})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Q
from users.models import User

@login_required
def chat_list(request):
    # Get all users the current user has chatted with
    sent = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    chat_users_ids = set(list(sent) + list(received))
    chat_users = User.objects.filter(id__in=chat_users_ids)
    
    return render(request, 'chat/chat_list.html', {'chat_users': chat_users})

@login_required
def chat_detail(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('chat_detail', username=username)
            
    return render(request, 'chat/chat_detail.html', {'other_user': other_user, 'chat_messages': messages})

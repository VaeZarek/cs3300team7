from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import User
from messaging.models import Message
from messaging.forms import MessageForm

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
def sent_messages(request):
    messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'messaging/sent_messages.html', {'messages': messages})

@login_required
def compose_message(request, recipient_id=None):
    recipient = None
    if recipient_id:
        recipient = get_object_or_404(User, pk=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = form.cleaned_data['recipient']
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm(initial={'recipient': recipient})
    return render(request, 'messaging/compose_message.html', {'form': form, 'recipient': recipient})

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    if message.recipient == request.user:
        message.read = True
        message.save()
        return render(request, 'messaging/view_message.html', {'message': message})
    elif message.sender == request.user:
        return render(request, 'messaging/view_message.html', {'message': message})
    else:
        return redirect('inbox') # Or handle permission denied
    
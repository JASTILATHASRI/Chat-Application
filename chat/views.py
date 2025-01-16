from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Message
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'chat/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'chat/login.html')


@login_required
def home(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/home.html', {'users': users})

@login_required
def chat_view(request, user_id):
    user = User.objects.get(id=user_id)
    messages = Message.objects.filter(sender=request.user, receiver=user) | \
              Message.objects.filter(sender=user, receiver=request.user)
    messages = messages.order_by('timestamp')

    if request.method == 'POST':
        message_content = request.POST['message']
        Message.objects.create(sender=request.user, receiver=user, content=message_content)
        return redirect('chat', user_id=user.id)

    return render(request, 'chat/chat.html', {'user': user, 'messages': messages})

@login_required
def home(request):
    users = User.objects.exclude(id=request.user.id)

    online_users = User.objects.filter(is_active=True).exclude(id=request.user.id)

    return render(request, 'chat/home.html', {'users': online_users})

def logout_view(request):
    logout(request)
    return redirect('home')
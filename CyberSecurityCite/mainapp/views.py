from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Event, Achievement
from django.contrib import messages

def home(request):
    return render(request, 'mainapp/home.html')

def events(request):
    all_events = Event.objects.all()
    return render(request, 'mainapp/events.html', {'events': all_events})

def achievements(request):
    all_achievements = Achievement.objects.all()
    return render(request, 'mainapp/achievements.html', {'achievements': all_achievements})

def contact(request):
    return render(request, 'mainapp/contact.html')

from .models import TeamMember

def team(request):
    members = TeamMember.objects.all()
    return render(request, 'mainapp/team.html', {'members': members})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'mainapp/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')


        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! You can now login.")
        return redirect('login')

    return render(request, 'mainapp/register.html')


def logout_view(request):
    logout(request)
    return redirect('home')

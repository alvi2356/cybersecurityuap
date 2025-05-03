from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Event, Achievement, TeamMember, FormerPresident, EventRegistration
from django.contrib import messages
from datetime import date
from django.db.utils import IntegrityError


def home(request):
    return render(request, 'mainapp/home.html')


def events(request):
    today = date.today()

    # Get all events and sort them by date
    all_events = Event.objects.all().order_by('date')

    # Split events into upcoming and past
    upcoming_events = [event for event in all_events if event.date >= today]
    past_events = [event for event in all_events if event.date < today]

    context = {
        'events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'mainapp/events.html', context)


def event_register(request, event_id):
    event = get_object_or_404(Event, eventID=event_id)

    if request.method == 'POST':
        # Extract form data
        full_name = request.POST.get('fullName')
        student_id = request.POST.get('studentId')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        semester = request.POST.get('semester')
        experience = request.POST.get('experience') == 'yes'
        expectations = request.POST.get('expectations')

        # Check if student is already registered for this event
        existing_registration = EventRegistration.objects.filter(event=event, student_id=student_id).exists()
        if existing_registration:
            messages.error(request, "You have already registered for this event.")
            return redirect('event_register', event_id=event_id)
            
        try:
            # Create registration in database
            registration = EventRegistration(
                event=event,
                full_name=full_name,
                student_id=student_id,
                email=email,
                phone=phone,
                department=department,
                semester=semester,
                has_experience=experience,
                expectations=expectations
            )
            registration.save()

            messages.success(request, "Registration successful! We'll contact you with more details soon.")
            return redirect('event_register', event_id=event.eventID)
        except IntegrityError:
            messages.error(request, "You have already registered for this event.")
            return redirect('event_register', event_id=event_id)

    context = {
        'event': event
    }
    return render(request, 'mainapp/eventregistration.html', context)


def achievements(request):
    # Get all achievements and sort them by date
    all_achievements = Achievement.objects.all().order_by('-dateAchieved')

    context = {
        'achievements': all_achievements,
    }
    return render(request, 'mainapp/achievements.html', context)


def contact(request):
    return render(request, 'mainapp/contact.html')


def team(request):
    members = TeamMember.objects.all()
    return render(request, 'mainapp/team.html', {'members': members})


def formerpresident(request):
    presidents = FormerPresident.objects.all()
    return render(request, 'mainapp/formerpresident.html', {'presidents': presidents})


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
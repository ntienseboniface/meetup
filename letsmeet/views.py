from django.shortcuts import render, get_object_or_404
from .models import Meetop
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MeetopForm



# Meetup details
def meetop_details(request, slug):
    meetup = get_object_or_404(Meetop, slug=slug)
    return render(request, 'letsmeet/meetop_detail.html', {'meetup': meetup})

# Meetup list
def home(request):
    meetups = Meetop.objects.filter(activate = True)
    return render(request, 'letsmeet/home.html', {'meetups': meetups})

# user registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()                                 # save user
            # ── automatically log them in ───────────────────
            raw_password = form.cleaned_data.get('password1')  # password they just set
            user = authenticate(request,                      # email is USERNAME_FIELD
                                 email=user.email,
                                 password=raw_password)
            if user:
                login(request, user)                          # start a session
            messages.success(request, 'Welcome to Meetop!')
            return redirect('dashboard')                      # <‑‑ send to dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'letsmeet/register.html', {'form': form})


# User Login
def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'letsmeet/login.html', {'form': form})


# User Logout
def user_logout(request):
    logout(request)
    return redirect('home')

#Dashboard
@login_required
def dashboard(request):
    my_meetups = Meetop.objects.filter(user=request.user)
    return render(request, 'letsmeet/dashboard.html',
                  {'my_meetups': my_meetups})


@login_required
def meetop_creation(request):
    if request.method == 'POST':
        form = MeetopForm(request.POST, request.FILES)
        if form.is_valid():
            meetup = form.save(commit=False)
            meetup.user = request.user          # organizer = current user
            meetup.organizer_email = request.user.email
            meetup.save()
            messages.success(request, 'Meetup created!')
            return redirect('meetop_detail', slug=meetup.slug)
    else:
        form = MeetopForm()
    return render(request, 'letsmeet/createmeetop.html', {'form': form, 'create': True})

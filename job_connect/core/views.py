from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from applicant.forms import ApplicantProfileForm
from recruiter.forms import RecruiterProfileForm
from core.forms import ApplicantSignUpForm, RecruiterSignUpForm
from django.contrib.auth.decorators import login_required

def applicant_signup(request):
    if request.method == 'POST':
        form = ApplicantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the user

            # Get or create the 'Applicant' group
            applicant_group, created = Group.objects.get_or_create(name='Applicant')

            # Add the new user to the 'Applicant' group
            user.groups.add(applicant_group)

            login(request, user)
            return redirect('applicant:applicant_profile_create')
    else:
        form = ApplicantSignUpForm()
    return render(request, 'core/applicant_signup.html', {'form': form})

def recruiter_signup(request):
    if request.method == 'POST':
        form = RecruiterSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the recruiter user

            # Get or create the 'Recruiter' group
            recruiter_group, created = Group.objects.get_or_create(name='Recruiter')

            # Add the new user to the 'Recruiter' group
            user.groups.add(recruiter_group)

            login(request, user)
            return redirect('recruiter:recruiter_profile_create')
    else:
        form = RecruiterSignUpForm()
    return render(request, 'core/recruiter_signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_applicant():
                return redirect('applicant:applicant_dashboard') # Define applicant dashboard URL
            elif user.is_recruiter():
                return redirect('recruiter:recruiter_dashboard') # Define recruiter dashboard URL
            else:
                return redirect('core:home') # Default redirect
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def home(request):
    return render(request, 'core/index.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:home') # Redirect to homepage

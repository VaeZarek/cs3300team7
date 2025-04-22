from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from applicant.forms import ApplicantProfileForm
from recruiter.forms import RecruiterProfileForm
from core.forms import ApplicantSignUpForm, RecruiterSignUpForm
from django.contrib.auth.decorators import login_required

def applicant_signup(request):
    """
    Handles the applicant signup process.

    Args:
        request (django.http.HttpRequest): HttpRequest object.

    Returns:
        django.http.HttpResponse: HttpResponse object rendering the signup form or redirecting to the profile creation page.
    """
    if request.method == 'POST':
        form = ApplicantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # :no-index: Create the user

            # :no-index: Get or create the 'Applicant' group
            applicant_group, created = Group.objects.get_or_create(name='Applicant')

            # :no-index: Add the new user to the 'Applicant' group
            user.groups.add(applicant_group)

            login(request, user)
            return redirect('applicant:applicant_profile_create')
    else:
        form = ApplicantSignUpForm()
    return render(request, 'core/applicant_signup.html', {'form': form})

def recruiter_signup(request):
    """
    Handles the recruiter signup process.

    Args:
        request (django.http.HttpRequest): HttpRequest object.

    Returns:
        django.http.HttpResponse: HttpResponse object rendering the signup form or redirecting to the profile creation page.
    """
    if request.method == 'POST':
        form = RecruiterSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # :no-index: Create the recruiter user

            # :no-index: Get or create the 'Recruiter' group
            recruiter_group, created = Group.objects.get_or_create(name='Recruiter')

            # :no-index: Add the new user to the 'Recruiter' group
            user.groups.add(recruiter_group)

            login(request, user)
            return redirect('recruiter:recruiter_profile_create')
    else:
        form = RecruiterSignUpForm()
    return render(request, 'core/recruiter_signup.html', {'form': form})

def login_view(request):
    """
    Handles the login process.

    Args:
        request (django.http.HttpRequest): HttpRequest object.

    Returns:
        django.http.HttpResponse: HttpResponse object rendering the login form or redirecting to the appropriate dashboard.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_applicant():
                return redirect('applicant:applicant_dashboard') # :no-index: Define applicant dashboard URL
            elif user.is_recruiter():
                return redirect('recruiter:recruiter_dashboard') # :no-index: Define recruiter dashboard URL
            else:
                return redirect('core:home') # :no-index: Default redirect
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def home(request):
    """
    Renders the home page.

    Args:
        request (django.http.HttpRequest): HttpRequest object.

    Returns:
        django.http.HttpResponse: HttpResponse object rendering the home page.
    """
    return render(request, 'core/index.html')

@login_required
def logout_view(request):
    """
    Handles the logout process.

    Args:
        request (django.http.HttpRequest): HttpRequest object.

    Returns:
        django.http.HttpResponse: HttpResponse object redirecting to the home page.
    """
    logout(request)
    return redirect('core:home') # :no-index: Redirect to homepage

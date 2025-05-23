from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ApplicantProfile #, Experience, Education
from django.db import transaction
from .forms import ApplicantProfileForm, ExperienceFormSet, EducationFormSet
from application.models import Application
from django.urls import reverse

@login_required
def applicant_dashboard(request):
    """
    Displays the applicant dashboard.

    Args:
        request (HttpRequest): HttpRequest object.

    Returns:
        HttpResponse: HttpResponse object rendering the applicant dashboard.
    """
    return render(request, 'applicant/applicant_dashboard.html')

@login_required
def applicant_profile_create(request):
    """
    Creates a new applicant profile.

    Args:
        request (HttpRequest): HttpRequest object.

    Returns:
        HttpResponse: HttpResponse object rendering the profile creation form or redirecting to the profile view.
    """
    if hasattr(request.user, 'applicant_profile'):
        return redirect('applicant:applicant_profile_update') # :no-index: Profile already exists
    if request.method == 'POST':
        profile_form = ApplicantProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('applicant:applicant_dashboard')
    else:
        profile_form = ApplicantProfileForm()
    return render(request, 'applicant/applicant_profile_create.html', {'profile_form': profile_form})

@login_required
def applicant_profile_update(request):
    """
    Updates an existing applicant profile.

    Args:
        request (HttpRequest): HttpRequest object.

    Returns:
        HttpResponse: HttpResponse object rendering the profile update form or redirecting to the profile view.
    """
    profile = get_object_or_404(ApplicantProfile, user=request.user)
    if request.method == 'POST':
        profile_form = ApplicantProfileForm(request.POST, request.FILES, instance=profile)
        experience_formset = ExperienceFormSet(request.POST, instance=profile)
        education_formset = EducationFormSet(request.POST, instance=profile)

        profile_valid = profile_form.is_valid()
        experience_valid = True  # Assume valid if no forms
        education_valid = True    # Assume valid if no forms

        if experience_formset.total_form_count() > 0:
            experience_valid = experience_formset.is_valid()

        if education_formset.total_form_count() > 0:
            education_valid = education_formset.is_valid()

        if profile_valid and experience_valid and education_valid:
            profile.headline = profile_form.cleaned_data['headline']
            profile.summary = profile_form.cleaned_data['summary']
            if 'skills' in profile_form.cleaned_data:
                profile.skills.set(profile_form.cleaned_data['skills'])
            if 'resume' in profile_form.cleaned_data and profile_form.cleaned_data['resume']:
                profile.resume = profile_form.cleaned_data['resume']
            profile.save()
            experience_formset.save()
            education_formset.save()
            return redirect(reverse('applicant:applicant_profile_view'))
    else:
        profile_form = ApplicantProfileForm(instance=profile)
        experience_formset = ExperienceFormSet(instance=profile)
        education_formset = EducationFormSet(instance=profile)

    return render(request, 'applicant/applicant_profile_update.html', {
        'profile_form': profile_form,
        'experience_formset': experience_formset,
        'education_formset': education_formset,
    })


@login_required
def applicant_profile_view(request):
    """
    Displays an applicant profile.

    Args:
        request (HttpRequest): HttpRequest object.

    Returns:
        HttpResponse: HttpResponse object rendering the applicant profile.
    """
    try:
        profile = request.user.applicant_profile
        return render(request, 'applicant/applicant_profile_view.html', {'profile': profile})
    except ApplicantProfile.DoesNotExist:
        return redirect('applicant:applicant_profile_create')

@login_required
def applicant_applications(request):
    """
    Displays a list of applications submitted by the applicant.

    Args:
        request (HttpRequest): HttpRequest object.

    Returns:
        HttpResponse: HttpResponse object rendering the list of applications.
    """

    try:
        applicant_profile = request.user.applicant_profile
        applications = Application.objects.filter(applicant=applicant_profile).order_by('-application_date')
        return render(request, 'applicant/applicant_applications_list.html', {'applications': applications})
    except AttributeError:
        # Handle the case where the user doesn't have an ApplicantProfile
        applications = Application.objects.none()  # Empty queryset
        return render(request, 'applicant/applicant_applications_list.html', {'applications': applications})
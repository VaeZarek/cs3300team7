from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ApplicantProfile #, Experience, Education
from .forms import ApplicantProfileForm, ExperienceFormSet, EducationFormSet
from application.models import Application
# from django.urls import reverse

@login_required
def applicant_dashboard(request):
    """View for the applicant's main dashboard."""
    return render(request, 'applicant/applicant_dashboard.html')

@login_required
def applicant_profile_create(request):
    if hasattr(request.user, 'applicant_profile'):
        return redirect('applicant_profile_update') # Profile already exists
    if request.method == 'POST':
        profile_form = ApplicantProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('applicant_dashboard')
    else:
        profile_form = ApplicantProfileForm()
    return render(request, 'applicant/applicant_profile_create.html', {'profile_form': profile_form})

@login_required
def applicant_profile_update(request):
    profile = get_object_or_404(ApplicantProfile, user=request.user)
    if request.method == 'POST':
        profile_form = ApplicantProfileForm(request.POST, request.FILES, instance=profile)
        experience_formset = ExperienceFormSet(request.POST, instance=profile)
        education_formset = EducationFormSet(request.POST, instance=profile)
        if profile_form.is_valid() and experience_formset.is_valid() and education_formset.is_valid():
            profile_form.save()
            experience_formset.save()
            education_formset.save()
            return redirect('applicant_profile_view')
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
    try:
        profile = request.user.applicant_profile
        return render(request, 'applicant/applicant_profile_view.html', {'profile': profile})
    except ApplicantProfile.DoesNotExist:
        return redirect('applicant_profile_create')

@login_required
def applicant_applications(request):
    try:
        applicant_profile = request.user.applicant_profile
        applications = Application.objects.filter(applicant_profile=applicant_profile).order_by('-applied_date')
        return render(request, 'applicant/applicant_applications_list.html', {'applications': applications})
    except AttributeError:
        # Handle the case where the user doesn't have an ApplicantProfile
        applications = Application.objects.none()  # Empty queryset
        return render(request, 'applicant/applicant_applications_list.html', {'applications': applications})

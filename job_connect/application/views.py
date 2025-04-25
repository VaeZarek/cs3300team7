
from applicant.models import ApplicantProfile
from application.models import Application
from application.forms import ApplicationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from application.models import Application
from application.forms import ApplicationStatusForm
from job.models import Job
from django.http import HttpResponseForbidden

@login_required
def apply_for_job(request, job_id):
    """
    Allows an applicant to apply for a specific job.

    Args:
        request (django.http.HttpRequest): HttpRequest object.
        job_id (int): The ID of the job being applied for.

    Returns:
        django.shortcuts.render or django.shortcuts.redirect: Renders the application form or redirects to the confirmation page upon successful application.

    Raises:
        HttpResponseForbidden: If a recruiter attempts to apply for a job.
    """
    if hasattr(request.user, 'recruiter_profile'):
        return HttpResponseForbidden("Recruiters are not allowed to apply for jobs.")

    job = get_object_or_404(Job, pk=job_id)
    applicant_profile = get_object_or_404(ApplicantProfile, user=request.user)

    if Application.objects.filter(applicant=applicant_profile, job=job).exists():
        return render(request, 'application/already_applied.html', {'job': job})

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = applicant_profile
            application.job = job
            application.save()
            return redirect('application:application_confirmation', job_id=job.id)
    else:
        form = ApplicationForm(initial={'applicant': applicant_profile.id, 'job': job.id})
    return render(request, 'application/apply_form.html', {'form': form, 'job': job})
@login_required
def application_confirmation(request, job_id):
    """
    Renders the application confirmation page.

    Args:
        request (django.http.HttpRequest): HttpRequest object.
        job_id (int): The ID of the job for which the application was submitted.

    Returns:
        django.shortcuts.render: Renders the application confirmation page.
    """
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'application/application_confirmation.html', {'job': job})

class RecruiterRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to restrict access to views only to recruiters.
    """
    def test_func(self):
        """
        Checks if the current user is a recruiter.

        Returns:
            bool: True if the user is a recruiter, False otherwise.
        """
        return hasattr(self.request.user, 'recruiter_profile')

@login_required
def job_applications_list(request, job_id):
    """
    Lists all applications for a specific job. Accessible only to recruiters.

    Args:
        request (django.http.HttpRequest): HttpRequest object.
        job_id (int): The ID of the job for which applications are listed.

    Returns:
        django.shortcuts.render: Renders the list of applications for the job.
    """
    job = get_object_or_404(Job, pk=job_id, recruiter__user=request.user)
    applications = Application.objects.filter(job=job).select_related('applicant__user')
    return render(request, 'application/job_applications_list.html', {'job': job, 'applications': applications})

class ApplicationUpdateStatusView(RecruiterRequiredMixin, UpdateView):
    """
    Allows a recruiter to update the status of an application.
    """
    model = Application
    form_class = ApplicationStatusForm
    template_name = 'application/application_update_status.html'
    success_url = '/recruiter/jobs/{job_id}/applications/'
    context_object_name = 'application'

    def get_queryset(self):
        """
        Returns the queryset of applications that the current recruiter has access to.

        Returns:
            django.db.models.query.QuerySet: The queryset of applications.
        """
        return Application.objects.filter(job__recruiter__user=self.request.user)

    def get_success_url(self):
        """
        Returns the URL to redirect to after successfully updating the application status.

        Returns:
            str: The success URL.
        """
        return self.success_url.format(job_id=self.object.job.id)

@login_required
def application_detail(request, application_id):
    """
    Displays the details of a specific application.

    Args:
        request (django.http.HttpRequest): The HTTP request object.
        application_id (int): The ID of the application to display.

    Returns:
        django.shortcuts.render: Renders the application detail template.
    """
    application = get_object_or_404(Application, pk=application_id)
    return render(request, 'application/application_detail.html', {'application': application})

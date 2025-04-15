from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from job.models import Job
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

@login_required
def apply_for_job(request, job_id):
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
            return redirect('application_confirmation', job_id=job.id)
    else:
        form = ApplicationForm(initial={'applicant': applicant_profile.id, 'job': job.id})
    return render(request, 'application/apply_form.html', {'form': form, 'job': job})

@login_required
def application_confirmation(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'application/application_confirmation.html', {'job': job})

class RecruiterRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'recruiter_profile')

@login_required
def job_applications_list(request, job_id):
    job = get_object_or_404(Job, pk=job_id, recruiter__user=request.user)
    applications = Application.objects.filter(job=job).select_related('applicant__user')
    return render(request, 'application/job_applications_list.html', {'job': job, 'applications': applications})

class ApplicationUpdateStatusView(RecruiterRequiredMixin, UpdateView):
    model = Application
    form_class = ApplicationStatusForm
    template_name = 'application/application_update_status.html'
    success_url = '/recruiter/jobs/{job_id}/applications/'
    context_object_name = 'application'

    def get_queryset(self):
        return Application.objects.filter(job__recruiter__user=self.request.user)

    def get_success_url(self):
        return self.success_url.format(job_id=self.object.job.id)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView, FormView
from django.urls import reverse_lazy, reverse
from recruiter.models import RecruiterProfile
from recruiter.forms import RecruiterProfileForm
from job.models import Job
from job.forms import JobForm
from application.models import Application
from application.forms import ApplicationStatusForm  # You'll need to create this form

class RecruiterRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'recruiter_profile')

class JobCreateView(RecruiterRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'job/job_form.html'
    success_url = '/recruiter/jobs/' # Redirect to recruiter's job list

    def form_valid(self, form):
        form.instance.recruiter = self.request.user.recruiter_profile
        return super().form_valid(form)

class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = 'job/job_detail.html'
    context_object_name = 'job' # The job object will be available in the template as 'job'

    def get_queryset(self):
        # Only allow recruiters to view their own job details
        return Job.objects.filter(recruiter__user=self.request.user)

class JobUpdateView(RecruiterRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'job/job_form.html' # Use the same form template as create
    context_object_name = 'job'
    # Override get_queryset to ensure the recruiter can only update their own jobs
    def get_queryset(self):
        return Job.objects.filter(recruiter__user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('recruiter_job_detail', kwargs={'pk': self.object.pk})

class JobDeleteView(RecruiterRequiredMixin, DeleteView):
    model = Job
    template_name = 'job/job_confirm_delete.html'
    success_url = '/recruiter/jobs/' # Redirect to recruiter's job list after deletion
    context_object_name = 'job'

    # Override get_queryset to ensure the recruiter can only delete their own jobs
    def get_queryset(self):
        return Job.objects.filter(recruiter__user=self.request.user)

class ApplicationUpdateStatusView(RecruiterRequiredMixin, FormView):
    template_name = 'application/application_update_status.html'
    form_class = ApplicationStatusForm
    context_object_name = 'application'

    def get_object(self):
        return get_object_or_404(Application, pk=self.kwargs['pk'], job__recruiter__user=self.request.user)

    def get_success_url(self):
        return reverse('recruiter_job_applications_list') # Redirect back to the list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application'] = self.get_object()
        return context

    def form_valid(self, form):
        application = self.get_object()
        application.status = form.cleaned_data['status']
        application.save()
        return super().form_valid(form)

@login_required
def recruiter_dashboard(request):
    job_postings = Job.objects.filter(recruiter=request.user)  # Get recruiter's job postings
    applications = Application.objects.filter(job__recruiter=request.user) # Get applications to those jobs

    context = {
        'job_postings': job_postings,
        'applications': applications,
    }
    return render(request, 'recruiter/recruiter_dashboard.html', context)

@login_required
def recruiter_job_list(request):
    """View to display a list of jobs posted by the logged-in recruiter."""
    if hasattr(request.user, 'recruiter_profile'):
        jobs = Job.objects.filter(recruiter__user=request.user).order_by('-posted_date')
        return render(request, 'job/recruiter_job_list.html', {'jobs': jobs})
    else:
        return redirect('recruiter_profile_create') # Or handle appropriately

@login_required
def job_applications_list(request):
    """View to display applications for the logged-in recruiter's jobs."""
    if hasattr(request.user, 'recruiter_profile'):
        jobs = Job.objects.filter(recruiter__user=request.user)
        applications = Application.objects.filter(job__in=jobs).order_by('-created_at')
        return render(request, 'application/job_applications_list.html', {'applications': applications})
    else:
        return redirect('recruiter_profile_create') # Or handle appropriately

@login_required
def recruiter_profile_create(request):
    if hasattr(request.user, 'recruiter_profile'):
        return redirect('recruiter_profile_update') # Profile already exists
    if request.method == 'POST':
        profile_form = RecruiterProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('recruiter_dashboard')
    else:
        profile_form = RecruiterProfileForm()
    return render(request, 'recruiter/recruiter_profile_create.html', {'profile_form': profile_form})

@login_required
def recruiter_profile_update(request):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    if request.method == 'POST':
        profile_form = RecruiterProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('recruiter_profile_view')
    else:
        profile_form = RecruiterProfileForm(instance=profile)
    return render(request, 'recruiter/recruiter_profile_update.html', {'profile_form': profile_form})

@login_required
def recruiter_profile_view(request):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    return render(request, 'recruiter/recruiter_profile_view.html', {'profile': profile})

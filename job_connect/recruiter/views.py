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
from application.forms import ApplicationStatusForm


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

class JobCreateView(RecruiterRequiredMixin, CreateView):
    """
    Allows a recruiter to create a new job posting.
    """
    model = Job
    form_class = JobForm
    template_name = 'job/job_form.html'
    success_url = 'recruiter/jobs/' # :no-index: Redirect to recruiter's job list

    def form_valid(self, form):
        """
        Saves the form and associates the job with the current recruiter.

        Args:
            form: The form to be saved.

        Returns:
            django.shortcuts.redirect: A redirect to the success URL.
        """
        form.instance.recruiter = self.request.user.recruiter_profile
        return super().form_valid(form)

class JobDetailView(LoginRequiredMixin, DetailView):
    """
    Displays the details of a specific job to a recruiter.
    """
    model = Job
    template_name = 'job/job_detail.html'
    context_object_name = 'job' # :no-index: The job object will be available in the template as 'job'

    def get_queryset(self):
        """
        Filters the queryset to only include jobs posted by the current recruiter.

        Returns:
            django.db.models.query.QuerySet: The filtered queryset.
        """
        return Job.objects.filter(recruiter__user=self.request.user)

class JobUpdateView(RecruiterRequiredMixin, UpdateView):
    """
    Allows a recruiter to update an existing job posting.
    """
    model = Job
    form_class = JobForm
    template_name = 'job/job_form.html' # Use the same form template as create
    context_object_name = 'job'
    # Override get_queryset to ensure the recruiter can only update their own jobs
    def get_queryset(self):
        """
        Filters the queryset to only include jobs posted by the current recruiter.

        Returns:
            django.db.models.query.QuerySet: The filtered queryset.
        """
        return Job.objects.filter(recruiter__user=self.request.user)

    def get_success_url(self):
        """
        Returns the URL to redirect to after successful update.

        Returns:
            str: The URL to redirect to.
        """
        return reverse_lazy('recruiter_job_detail', kwargs={'pk': self.object.pk})

class JobDeleteView(RecruiterRequiredMixin, DeleteView):
    """
    Allows a recruiter to delete an existing job posting.
    """
    model = Job
    template_name = 'job/job_confirm_delete.html'
    success_url = 'recruiter/jobs/' # Redirect to recruiter's job list after deletion
    context_object_name = 'job'

    # Override get_queryset to ensure the recruiter can only delete their own jobs
    def get_queryset(self):
        """
        Filters the queryset to only include jobs posted by the current recruiter.

        Returns:
            django.db.models.query.QuerySet: The filtered queryset.
        """
        return Job.objects.filter(recruiter__user=self.request.user)

class ApplicationUpdateStatusView(RecruiterRequiredMixin, FormView):
    """
    Allows a recruiter to update the status of an application.
    """
    template_name = 'application/application_update_status.html'
    form_class = ApplicationStatusForm
    context_object_name = 'application'

    def get_object(self):
        """
        Gets the application object to be updated.

        Returns:
            application.models.Application: The application object.
        """
        return get_object_or_404(Application, pk=self.kwargs['pk'], job__recruiter__user=self.request.user)

    def get_success_url(self):
        """
        Returns the URL to redirect to after successful update.

        Returns:
            str: The URL to redirect to.
        """
        return reverse('recruiter:recruiter_job_applications_list') # Redirect back to the list

    def get_context_data(self, **kwargs):
        """
        Adds the application and the form to the context.

        Args:
            kwargs (dict): Keyword arguments.
        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context['application'] = self.get_object()
        return context

    def form_valid(self, form):
        """
        Saves the form and updates the application status.

        Args:
            form (application.forms.ApplicationStatusForm): The form to be saved.
        Returns:
            django.shortcuts.redirect: A redirect to the success URL.
        """
        application = self.get_object()
        application.status = form.cleaned_data['status']
        application.save()
        return super().form_valid(form)

@login_required
def recruiter_dashboard(request):
    """
    Displays the recruiter dashboard with relevant information.

    Args:
        request (django.http.HttpRequest): HttpRequest object.

    Returns:
        django.http.HttpResponse: HttpResponse object.
    """
    recruiter_profile = RecruiterProfile.objects.get(user=request.user)
    job_postings = Job.objects.filter(recruiter=recruiter_profile)
    applications = Application.objects.filter(job__recruiter=recruiter_profile) # Use recruiter_profile

    context = {
        'job_postings': job_postings,
        'applications': applications,
    }
    return render(request, 'recruiter/recruiter_dashboard.html', context)

@login_required
def recruiter_job_list(request):
    """
    Displays a list of jobs posted by the current recruiter.

    Args:
        request (django.http.HttpRequest): HttpRequest object.

    Returns:
        django.http.HttpResponse: HttpResponse object.
    """
    if hasattr(request.user, 'recruiter_profile'):
        jobs = Job.objects.filter(recruiter__user=request.user).order_by('-posted_date')
        return render(request, 'job/recruiter_job_list.html', {'jobs': jobs})
    else:
        return redirect('recruiter_profile_create') # Or handle appropriately

@login_required
def job_applications_list(request):
    """
    Displays a list of applications for a specific job.

    Args:
        request (django.http.HttpRequest): HttpRequest object.
        job_id (int): The ID of the job.

    Returns:
        django.http.HttpResponse: HttpResponse object.
    """
    if hasattr(request.user, 'recruiter_profile'):
        jobs = Job.objects.filter(recruiter__user=request.user)
        applications = Application.objects.filter(job__in=jobs).order_by('-created_at')
        return render(request, 'application/job_applications_list.html', {'applications': applications})
    else:
        return redirect('recruiter_profile_create') # Or handle appropriately

@login_required
def recruiter_profile_create(request):
    """
    Allows a recruiter to create their profile.

    Args:
        request (django.http.HttpRequest): HttpRequest object.

    Returns:
        django.http.HttpResponse: HttpResponse object.
    """
    if hasattr(request.user, 'recruiter_profile'):
        return redirect('recruiter:recruiter_profile_update') # Profile already exists
    if request.method == 'POST':
        profile_form = RecruiterProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('recruiter:recruiter_dashboard')
    else:
        profile_form = RecruiterProfileForm()
    return render(request, 'recruiter/recruiter_profile_create.html', {'profile_form': profile_form})

@login_required
def recruiter_profile_update(request):
    """
    Allows a recruiter to update their profile.

    Args:
        request (django.http.HttpRequest): HttpRequest object.

    Returns:
        django.http.HttpResponse: HttpResponse object.
    """
    try:
        profile = RecruiterProfile.objects.get(user=request.user)
    except RecruiterProfile.DoesNotExist:
        return redirect(reverse('recruiter:recruiter_profile_create'))

    if request.method == 'POST':
        profile_form = RecruiterProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('recruiter:recruiter_profile_view'))
    else:
        profile_form = RecruiterProfileForm(instance=profile)
    return render(request, 'recruiter/recruiter_profile_update.html', {'profile_form': profile_form})

@login_required
def recruiter_profile_view(request):
    """
    Displays the recruiter profile.

    Args:
        request (django.http.HttpRequest): HttpRequest object.

    Returns:
        django.http.HttpResponse: HttpResponse object.
    """

    profile = get_object_or_404(RecruiterProfile, user=request.user)
    return render(request, 'recruiter/recruiter_profile_view.html', {'profile': profile})

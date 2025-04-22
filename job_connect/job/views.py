from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from job.models import Job
from job.forms import JobForm
from django.db.models import Q
from django.urls import reverse, reverse_lazy


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

    def handle_no_permission(self):
        """
        Handles the case where the user does not have permission to access the view.
        """

        if self.request.user.is_authenticated:
            return redirect(reverse('recruiter:recruiter_profile_create'))
        return super().handle_no_permission()

class JobListView(ListView):
    """
    Displays a list of all active jobs.
    """
    model = Job
    template_name = 'job/job_list.html'
    context_object_name = 'jobs'
    ordering = ['-posted_date']

class JobDetailView(DetailView):
    """
    Displays the details of a specific job.
    """
    model = Job
    template_name = 'job/job_detail.html'
    context_object_name = 'job'

class JobCreateView(RecruiterRequiredMixin, CreateView):
    """
    Allows a recruiter to create a new job posting.
    """
    model = Job
    form_class = JobForm
    template_name = 'job/job_form.html'
    success_url = reverse_lazy('job:recruiter_job_list')

    def form_valid(self, form):
        """
        Saves the form and associates the job with the current recruiter.

        Args:
            form (job.forms.JobForm): The form to be saved.

        Returns:
            django.shortcuts.redirect: A redirect to the success URL.
        """
        form.instance.recruiter = self.request.user.recruiter_profile
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

class JobUpdateView(UpdateView):
    """
    Allows a recruiter to update an existing job posting.
    """

    model = Job
    form_class = JobForm
    template_name = 'job/job_form.html'
    success_url = reverse_lazy('job:recruiter_job_list')
    context_object_name = 'job'

    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the current user has permission to update the job.

        Args:
            request (django.http.HttpRequest): HttpRequest object.

        Returns:
            django.http.HttpResponse: HttpResponse or HttpResponseForbidden
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission(request)

        if not hasattr(request.user, 'recruiter_profile'):
            recruiter_mixin = RecruiterRequiredMixin()
            recruiter_mixin.request = request
            return recruiter_mixin.handle_no_permission()  # :no-index: Do not pass request here

        job = get_object_or_404(Job, pk=kwargs['pk'])
        if job.recruiter.user != request.user:
            return HttpResponseForbidden("You are not authorized to update this job.")

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self, request):
        """
        Handles the case where the user does not have permission to access the view.
        """
        return redirect('core:login') # :no-index: Or your login URL name

    def form_valid(self, form):
        """
        Saves the form.

        Args:
            form (job.forms.JobForm): The form to be saved.

        Returns:
            django.shortcuts.redirect: A redirect to the success URL.
        """
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

class JobDeleteView(LoginRequiredMixin, DeleteView):
    """
    Allows a recruiter to delete an existing job posting.
    """
    model = Job
    template_name = 'job/job_confirm_delete.html'
    success_url = '/jobs/recruiter/jobs/'
    context_object_name = 'job'

    def dispatch(self, request, *args, **kwargs):
        """
        Allows a recruiter to delete an existing job posting.
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission(request)

        if not hasattr(request.user, 'recruiter_profile'):
            recruiter_mixin = RecruiterRequiredMixin()
            recruiter_mixin.request = request
            return recruiter_mixin.handle_no_permission() # :no-index: Do not pass request here

        job = get_object_or_404(Job, pk=kwargs['pk'])
        if job.recruiter.user != request.user:
            raise Http404("You are not authorized to delete this job.")

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self, request):
        """
        Handles the case where the user does not have permission to access the view.
        """
        return redirect('core:login') # :no-index: Replace 'your_login_url_name'


class JobSearchView(ListView):
    """
    Displays a list of jobs that match a search query.
    """
    model = Job
    template_name = 'job/job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        """
        Filters the queryset based on the search query.

        Returns:
            django.db.models.query.QuerySet: The filtered queryset.
        """
        query = self.request.GET.get('q')
        if query:
            return Job.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query) | Q(skills_required__name__icontains=query)
            ).distinct().order_by('-posted_date')
        return Job.objects.all().order_by('-posted_date')

    def get_context_data(self, **kwargs):
        """
        Adds the search query to the context.

        Args:
            kwargs (dict): Keyword arguments.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class RecruiterJobList(RecruiterRequiredMixin, ListView):
    """
    Displays a list of jobs posted by a specific recruiter.
    """
    model = Job
    template_name = 'job/recruiter_job_list.html'
    context_object_name = 'jobs'
    ordering = ['-posted_date']

    def get_queryset(self):
        """
        Filters the queryset to only include jobs posted by the current recruiter.

        Returns:
            django.db.models.query.QuerySet: The filtered queryset.
        """
        return Job.objects.filter(recruiter=self.request.user.recruiter_profile).order_by('-posted_date')
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from job.models import Job
from job.forms import JobForm
from django.db.models import Q
from django.urls import reverse



class RecruiterRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'recruiter_profile')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect(reverse('recruiter:recruiter_profile_create'))
        return super().handle_no_permission()

class JobListView(ListView):
    model = Job
    template_name = 'job/job_list.html'
    context_object_name = 'jobs'
    ordering = ['-posted_date']

class JobDetailView(DetailView):
    model = Job
    template_name = 'job/job_detail.html'
    context_object_name = 'job'

class JobCreateView(RecruiterRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'job/job_form.html'
    success_url = '/recruiter/jobs/' # Redirect to recruiter's job list

    def form_valid(self, form):
        form.instance.recruiter = self.request.user.recruiter_profile
        return super().form_valid(form)

class JobUpdateView(RecruiterRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'job/job_form.html'
    success_url = 'recruiter/jobs/'
    context_object_name = 'job'

    def test_func(self):
        job = self.get_object()
        return job.recruiter.user == self.request.user

class JobDeleteView(RecruiterRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'job/job_confirm_delete.html'
    success_url = '/jobs/recruiter/jobs/'  # Ensure leading slash for consistency with reverse()
    context_object_name = 'job'

    def test_func(self, user):
        try:
            job = self.get_object()
        except Http404:
            return False
        return job.recruiter.user == user

    def handle_no_permission(self):
        raise Http404("You are not authorized to delete this job.")

@login_required
def recruiter_job_list(request):
    if hasattr(request.user, 'recruiter_profile'):
        jobs = Job.objects.filter(recruiter__user=request.user).order_by('-posted_date')
        return render(request, 'job/recruiter_job_list.html', {'jobs': jobs})
    else:
        return redirect('recruiter:recruiter_profile_create') # Or handle appropriately

class JobSearchView(ListView):
    model = Job
    template_name = 'job/job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Job.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query) | Q(skills_required__name__icontains=query)
            ).distinct().order_by('-posted_date')
        return Job.objects.all().order_by('-posted_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

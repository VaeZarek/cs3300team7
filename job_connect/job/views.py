from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from job.models import Job
from job.forms import JobForm
from django.db.models import Q
from django.urls import reverse
from django.views.generic import DeleteView as BaseDeleteView

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
    success_url = '/jobs/recruiter/jobs/'

    def form_valid(self, form):
        form.instance.recruiter = self.request.user.recruiter_profile
        return super().form_valid(form)

class JobUpdateView(UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'job/job_form.html'
    success_url = '/recruiter/jobs/'
    context_object_name = 'job'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission(request) # Use the view's handle_no_permission

        if not hasattr(request.user, 'recruiter_profile'):
            recruiter_mixin = RecruiterRequiredMixin()
            recruiter_mixin.request = request
            return recruiter_mixin.handle_no_permission(request)

        job = get_object_or_404(Job, pk=kwargs['pk'])
        if job.recruiter.user != request.user:
            return HttpResponseForbidden("You are not authorized to update this job.")

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self, request):
        return redirect('login') # Or your login URL name

class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'job/job_confirm_delete.html'
    success_url = '/jobs/recruiter/jobs/'
    context_object_name = 'job'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not hasattr(request.user, 'recruiter_profile'):
            recruiter_mixin = RecruiterRequiredMixin()
            recruiter_mixin.request = request
            return recruiter_mixin.handle_no_permission(request)

        job = get_object_or_404(Job, pk=kwargs['pk'])
        if job.recruiter.user != request.user:
            raise Http404("You are not authorized to delete this job.")

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect('login') # Or your login URL name

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

class RecruiterJobList(RecruiterRequiredMixin, ListView):
    model = Job
    template_name = 'job/recruiter_job_list.html'
    context_object_name = 'jobs'
    ordering = ['-posted_date']

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user.recruiter_profile).order_by('-posted_date')
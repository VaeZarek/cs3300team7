from django.urls import path
from . import views

urlpatterns = [
    path('profile/create/', views.recruiter_profile_create, name='recruiter_profile_create'),
    path('profile/update/', views.recruiter_profile_update, name='recruiter_profile_update'),
    path('profile/', views.recruiter_profile_view, name='recruiter_profile_view'),
    path('dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'), # Example dashboard
    path('jobs/', views.recruiter_job_list, name='recruiter_job_list'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job_create'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('jobs/<int:pk>/update/', views.JobUpdateView.as_view(), name='job_update'),
    path('jobs/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
    path('jobs/<int:job_id>/applications/', views.job_applications_list, name='job_applications_list'),
    path('applications/<int:pk>/update_status/', views.ApplicationUpdateStatusView.as_view(), name='application_update_status'),
]

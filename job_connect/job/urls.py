from django.urls import path
from . import views

app_name = 'job'

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('search/', views.JobSearchView.as_view(), name='job_search'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('create/', views.JobCreateView.as_view(), name='job_create'),
    path('recruiter/jobs/', views.recruiter_job_list, name='recruiter_job_list'),
    path('<int:pk>/update/', views.JobUpdateView.as_view(), name='job_update'),  # Add this
    path('<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),  # Add this
]
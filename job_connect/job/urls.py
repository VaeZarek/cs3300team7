from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

app_name = 'job'

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('search/', views.JobSearchView.as_view(), name='job_search'),
    path('create/', views.JobCreateView.as_view(), name='job_create'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'), # Keep this if you want public job details here
    path('<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_update'),
    path('<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'), 
]

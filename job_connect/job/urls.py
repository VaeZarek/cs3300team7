from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('search/', views.JobSearchView.as_view(), name='job_search'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'), # Keep this if you want public job details here
]

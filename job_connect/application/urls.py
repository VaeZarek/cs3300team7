from django.urls import path
from . import views

app_name = 'application'

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('confirmation/<int:job_id>/', views.application_confirmation, name='application_confirmation'),
    # :no-index: You might add URLs for an applicant to view their applications here
]

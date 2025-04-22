from django.urls import path
from . import views

app_name = 'applicant'

urlpatterns = [
    path('dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('profile/create/', views.applicant_profile_create, name='applicant_profile_create'),
    path('profile/update/', views.applicant_profile_update, name='applicant_profile_update'),
    path('profile/', views.applicant_profile_view, name='applicant_profile_view'),
    path('applications/', views.applicant_applications, name='applicant_applications'),  # THIS LINE IS CRUCIAL
    # ... any other URL patterns for the applicant app
]


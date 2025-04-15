from django.urls import path
from . import views

urlpatterns = [
    path('signup/applicant/', views.applicant_signup, name='applicant_signup'),
    path('signup/recruiter/', views.recruiter_signup, name='recruiter_signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
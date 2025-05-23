from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('signup/applicant/', views.applicant_signup, name='applicant_signup'),
    path('signup/recruiter/', views.recruiter_signup, name='recruiter_signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),

]

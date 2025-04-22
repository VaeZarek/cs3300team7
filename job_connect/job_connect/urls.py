from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls), # :no-index: Django Administration
    path('', include('core.urls', namespace='core')),
    path('applicant/', include('applicant.urls', namespace='applicant')),
    path('recruiter/', include('recruiter.urls', namespace='recruiter')),
    path('jobs/', include('job.urls', namespace='job')),
    path('applications/', include('application.urls', namespace='application')),
    # path('messages/', include('messaging.urls', namespace='messaging')), # Uncomment and namespace if you have this app
]
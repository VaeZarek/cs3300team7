"""
URL configuration for job_connect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

**Examples:**

Function views:

1.  Add an import: ``from my_app import views``
2.  Add a URL to urlpatterns: ``path('', views.home, name='home')``

Class-based views:

1.  Add an import: ``from other_app.views import Home``
2.  Add a URL to urlpatterns: ``path('', Home.as_view(), name='home')``

Including another URLconf:

1.  Import the include() function: ``from django.urls import include, path``
2.  Add a URL to urlpatterns: ``path('blog/', include('blog.urls'))``
"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls), # Django Administration
    path('', include('core.urls', namespace='core')),
    path('applicant/', include('applicant.urls', namespace='applicant')),
    path('recruiter/', include('recruiter.urls', namespace='recruiter')),
    path('jobs/', include('job.urls', namespace='job')),
    path('applications/', include('application.urls', namespace='application')),
    # path('messages/', include('messaging.urls', namespace='messaging')), # Uncomment and namespace if you have this app
]


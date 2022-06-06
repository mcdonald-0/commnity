from django.urls import path

from issues.views import *

app_name = 'issues'
urlpatterns = [
    path('report_an_issue/', report_an_issue, name='report_an_issue'),
]
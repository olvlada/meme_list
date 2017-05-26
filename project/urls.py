from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from . import api


urlpatterns = [
    url(r'^api/upload_file$', api.FileUploadView.as_view()),
    url(r'^$', TemplateView.as_view(template_name='main.html')),
]

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from . import api
from . import views


urlpatterns = [
    url(r'^api/upload_file$', api.FileUploadView.as_view()),
    url(r'^$', TemplateView.as_view(template_name='main.html')),
    url(r'^api/export_to_jpg$', api.ExportToJpgView.as_view()),
    url(r'^export_to_jpg/(?P<file_code>[0-9]+)$', views.export_to_jpg),
]

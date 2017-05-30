import os
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def export_to_jpg(request, file_code):
    file_path = 'tmp/{}.jpg'.format(file_code)
    response_file = open(file_path, 'rb')
    response = HttpResponse(content=response_file.read())
    response['Content-Type'] = 'application/octed-stream'
    response['Content-Disposition'] = 'attachment; filename="export.jpg"'
    response_file.close()
    os.remove(file_path)
    return response
    
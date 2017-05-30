import imgkit
import random
import json
from django.shortcuts import render
from django.views.generic import View
from django.template import loader, Context
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from parsers import FileParser, RowParser


class FileUploadView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        files = request.FILES

        result = []
        for file in files.values():
            parser = FileParser(file, RowParser())
            result += parser.parse()

        return Response({'data': result}, status=200)


class ExportToJpgView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        result_data = json.loads(request.body)
        template = loader.get_template('export.html')
        context = Context({'data': result_data})
        file_code = random.randint(0, 999999999)
        file_path = 'tmp/{}.jpg'.format(file_code)
        imgkit.from_string(template.render(context), file_path)
        return Response({'file_code': file_code}, status=200)

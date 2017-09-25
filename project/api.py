import imgkit
import random
import json
import requests

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

    def init_images(self, list_data, key_name):
        """
        Set initial images for response data.  Needs for template conditions.   
        """
        for item in list_data:
            item[key_name] = item.get(key_name, None)
        return list_data

    def post(self, request, *args, **kwargs):
        result_data = json.loads(request.body)
        for result_item in result_data:
            result_item['custom_domain_image'] = result_item.get('customDomainImage', None)
            result_item['show_site_image'] = True
            if not result_item['custom_domain_image']:
                site_logo = requests.get('http://logo.clearbit.com/{}?size=50'.format(result_item['domain']))
                if site_logo.status_code != 200:
                    result_item['show_site_image'] = False

            if result_item.get('verticals', None):
                self.init_images(result_item['verticals'], 'customVerticalImage')

            if result_item.get('geos', None):
                self.init_images(result_item['geos'], 'customGeoImage')

            if result_item.get('sizes', None):
                result_item['sizes'] = [size['name'] for size in result_item['sizes']]

        template = loader.get_template('export.html')
        context = Context({'data': result_data})
        file_code = random.randint(0, 999999999)
        file_path = 'tmp/{}.jpg'.format(file_code)
        imgkit.from_string(template.render(context), file_path)
        return Response({'file_code': file_code}, status=200)


class ExportIcons(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        code_list = ['US', 'UK', 'CA', 'AU', 'JP', 'FR', 'MX', 'ES', 'AR', 'BR', 'PT', 'MZ', 'AO', 'CO', 'VE', 'CZ', 'PE']
        color_list = [
            {'color': '#03080e', 'type': 'dark'},
            {'color': '#2a404b', 'type': 'light'}
        ]

        for code in code_list:
            for color in color_list:
                template = loader.get_template('icon.html')
                context = Context({'code': code, 'color': color['color']})
                file_path = 'tmp/{}-{}.png'.format(code, color['type'])
                imgkit.from_string(
                    template.render(context),
                    file_path, 
                    options={
                        'format': 'png',
                        'crop-h': '29',
                        'crop-w': '28',
                        'crop-x': '0',
                        'crop-y': '0',
                        'quality': '100'
                    }
                )
        
        return Response({'test': 1}, status=200)

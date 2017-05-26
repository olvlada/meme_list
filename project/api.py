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

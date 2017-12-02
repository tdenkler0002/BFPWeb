from django.views import generic
from django.shortcuts import render, redirect
from rest_framework import generics
from .serializers import DocumentSerializer
from .models import Document, DocumentForm
from . import BFParser
from .settings.base import *
from django.core.files import File
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
import os
from django.conf import settings
from annoying.decorators import ajax_request

class FileView(generics.ListCreateAPIView):
  queryset = Document.objects.all()
  serializer_class = DocumentSerializer
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    contentTypes=['application/json', 'application/csv', 'application/xml', 'text/csv']
    doc_serializer = DocumentSerializer(data=request.data)
    uploadedFile = request.FILES['file']
    # Parse the CSV file according to rules
    BFParser.PyParser(uploadedFile)

    # Check that file type is JSON, CSV, or XML
    if doc_serializer.is_valid() and uploadedFile.content_type in contentTypes:
      doc_serializer.save()
      return Response(doc_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(doc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class documentList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'

    def get(self, request):
        queryset = Document.objects.all()
        return Response({'documents': queryset})


class HomePage(generic.TemplateView):
    template_name = "home.html"

    @ajax_request
    def json_files(request, dir_name):
        path = os.path.join(settings.MEDIA_ROOT, dir_name)
        files = []
        for f in os.listdir(path):
            if f.endswith("csv") or f.endswith("Corrected"): # to avoid other files
                files.append("%s%s/%s" % (settings.MEDIA_URL, dir_name, f)) # modify the concatenation to fit your neet
        return {'files': files}

class AboutPage(generic.TemplateView):
    template_name = "about.html"

class SuccessPage(generic.TemplateView):
    template_name = "sucess.html"

# class download(request, file_name):
#     file_path = settings.base.MEDIA_ROOT +'/'+ file_name
#     print(file_path)
#     file_wrapper = FileWrapper(file(file_path,'rb'))
#     file_mimetype = mimetypes.guess_type(file_path)
#     response = HttpResponse(file_wrapper, content_type=file_mimetype )
#     response['X-Sendfile'] = file_path
#     response['Content-Length'] = os.stat(file_path).st_size
#     response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
#     #return response

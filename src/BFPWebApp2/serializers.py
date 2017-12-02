from rest_framework import serializers
from BFPWebApp2.models import Document

""" Serializer to map the Model instance into JSON """
class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('document_id', 'file')

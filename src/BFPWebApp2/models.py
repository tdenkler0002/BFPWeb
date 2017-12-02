from django.db import models
from django.forms import ModelForm


class Document(models.Model):
    document_id=models.AutoField(primary_key=True)
    file = models.FileField(upload_to='documents')

class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('file',)

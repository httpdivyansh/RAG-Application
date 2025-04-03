
from django.db import models
from django.contrib.auth.models import User

class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pdf_file.name

class auth_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL , null=True , blank= True)

# C:\Users\700067\Desktop\rag_project\myproject\docai\forms.py
from django import forms
from .models import UploadedPDF

class PDFForm(forms.ModelForm):
    class Meta:
        model = UploadedPDF
        fields = ['pdf_file']

class QueryForm(forms.Form):
    query = forms.CharField(label='Enter your question', max_length=500)
    model_choice = forms.ChoiceField(
        choices=[
            ('llama3-70b-8192', 'LLaMA 3 70B'),
            ('deepseek-r1-distill-llama-70b', 'Deepseek'),
        ],
        label='Select Model'
    )
from django import forms
from .models import CertificateTemplate

class CertificateTemplateForm(forms.ModelForm):
    class Meta:
        model = CertificateTemplate
        fields = ['name', 'html_content']

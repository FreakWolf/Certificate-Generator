from django.db import models
from django.utils.crypto import get_random_string

class CertificateTemplate(models.Model):
    name = models.CharField(max_length=100)
    html_content = models.TextField()
    
    def __str__(self):
        return self.name

class Certificate(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    completion_date = models.DateField()
    certificate_code = models.CharField(max_length=10, unique=True)
    pdf_file = models.FileField(upload_to='certificates/')

    def save(self, *args, **kwargs):
        if not self.certificate_code:
            self.certificate_code = get_random_string(length=10).upper()
        super().save(*args, **kwargs)
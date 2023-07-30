from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.conf import settings
from bs4 import BeautifulSoup
import os
import jwt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import Certificate, CertificateTemplate

def landing_page(request):
    return render(request, 'landing_page.html')

def generate_certificate(request):
    templates = CertificateTemplate.objects.all()
    
    if request.method == 'POST':
        selected_template_id = request.POST.get('template')
        selected_template = CertificateTemplate.objects.get(pk=selected_template_id)
        
        name = request.POST.get('name')
        course = request.POST.get('course')
        completion_date = request.POST.get('completion_date')

        # Create and save the certificate to the database
        certificate = Certificate(name=name, course=course, completion_date=completion_date)
        certificate.save()

        # Generate and save the PDF certificate
        pdf_buffer = BytesIO()
        generate_pdf_certificate(pdf_buffer, selected_template.html_content, name, course, completion_date)
        certificate.pdf_file.save(f'{certificate.certificate_code}.pdf', ContentFile(pdf_buffer.getvalue()))

        return HttpResponse('Certificate generated successfully!', status=201, content_type='text/plain')
    return render(request, 'certificate_generator.html', { 'templates': templates })

def verify_certificate(request):
    if request.method == 'POST':
        certificate_code = request.POST.get('certificate_code')

        try:
            certificate = Certificate.objects.get(certificate_code=certificate_code)

            # Generate a JWT for verification (for bonus)
            verification_token = jwt.encode({'certificate_code': certificate.certificate_code}, settings.SECRET_KEY, algorithm='HS256')

            return HttpResponse(f'Certificate is valid. Verification Token: {verification_token}')
        except ObjectDoesNotExist:
            return HttpResponse('Invalid certificate code')
    return render(request, 'certificate_verification.html')

def generate_pdf_certificate(buffer, html_content, name, course, completion_date):
    c = canvas.Canvas(buffer, pagesize=letter)
    
    soup = BeautifulSoup(html_content, 'html.parser')

    # Certificate content
    c.setFont("Helvetica", 20)
    c.drawCentredString(300, 700, "Certificate of Completion")
    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 650, "This is to certify that")
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(300, 600, name)
    c.setFont("Helvetica", 16)
    c.drawCentredString(300, 550, "has successfully completed the course")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, 500, course)
    c.setFont("Helvetica", 14)
    c.drawCentredString(300, 450, f"Date of Completion: {completion_date}")

    c.save()

# Add URL patterns to the certificate_app/urls.py file.
# (Assuming you have already created templates for certificate_generator.html and certificate_verification.html)

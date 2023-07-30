from django.urls import path
from . import views

urlpatterns = [
    path('generate-certificate/', views.generate_certificate, name='generate_certificate'),
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
]

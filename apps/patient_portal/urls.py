from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.portal_dashboard, name='dashboard'),
    path('documents/', views.portal_documents, name='documents'),
    path('documents/<int:pk>/', views.portal_document_detail, name='document_detail'),
    path('appointments/', views.portal_appointments, name='appointments'),
    path('appointments/request/', views.portal_request_appointment, name='request_appointment'),
    path('prescriptions/', views.portal_prescriptions, name='prescriptions'),
    path('publish/<int:patient_id>/', views.publish_document, name='publish'),
]

from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.patient_list, name='list'),
    path('new/', views.patient_create, name='create'),
    path('<int:pk>/', views.patient_detail, name='detail'),
    path('<int:pk>/edit/', views.patient_edit, name='edit'),
    path('<int:pk>/allergies/add/', views.allergy_add, name='allergy_add'),
    path('<int:pk>/allergies/<int:allergy_id>/delete/', views.allergy_delete, name='allergy_delete'),
    path('<int:pk>/alerts/add/', views.alert_add, name='alert_add'),
    path('<int:pk>/history/', views.history_save, name='history_save'),
    path('<int:pk>/documents/upload/', views.document_upload, name='document_upload'),
    path('<int:pk>/documents/<int:doc_id>/download/', views.document_download, name='document_download'),
]

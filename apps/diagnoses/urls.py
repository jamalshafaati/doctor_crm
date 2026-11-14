from django.urls import path
from . import views
app_name = 'diagnoses'
urlpatterns = [
    path('', views.diagnosis_list, name='list'),
]

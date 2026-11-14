from django.urls import path
from . import views
from . import clinical_actions as actions

app_name = 'encounters'

urlpatterns = [
    path('', views.encounter_list, name='list'),
    path('new/', views.encounter_create, name='create'),
    path('<int:pk>/', views.encounter_workspace, name='workspace'),
    path('<int:pk>/report/', views.encounter_report, name='report'),
    path('<int:pk>/finalize/', views.encounter_finalize, name='finalize'),
    path('<int:pk>/notes/', actions.update_notes, name='update_notes'),
    path('<int:pk>/diagnosis/', actions.add_diagnosis, name='add_diagnosis'),
    path('<int:pk>/treatment/', actions.add_treatment, name='add_treatment'),
    path('<int:pk>/prescription/', actions.add_prescription, name='add_prescription'),
    path('<int:pk>/prescription/<int:rx_id>/approve/', actions.approve_prescription, name='approve_prescription'),
]

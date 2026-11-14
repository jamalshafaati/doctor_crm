from django.urls import path
from . import views

app_name = 'foot_ankle'

urlpatterns = [
    path('encounter/<int:encounter_id>/exam/<str:exam_type>/', views.add_exam, name='add_exam'),
]

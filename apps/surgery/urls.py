from django.urls import path
from . import views

app_name = 'surgery'

urlpatterns = [
    path('', views.surgery_list, name='list'),
    path('new/', views.surgery_create, name='create'),
    path('<int:pk>/', views.surgery_detail, name='detail'),
    path('<int:pk>/edit/', views.surgery_edit, name='edit'),
    path('<int:surgery_id>/implants/add/', views.implant_add, name='implant_add'),
]

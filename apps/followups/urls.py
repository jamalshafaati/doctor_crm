from django.urls import path
from . import views

app_name = 'followups'

urlpatterns = [
    path('', views.followup_list, name='list'),
    path('new/', views.followup_create, name='create'),
    path('<int:pk>/', views.followup_detail, name='detail'),
    path('<int:pk>/edit/', views.followup_edit, name='edit'),
]

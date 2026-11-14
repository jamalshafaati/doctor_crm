from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_list, name='list'),
    path('calendar/', views.appointment_calendar, name='calendar'),
    path('new/', views.appointment_create, name='create'),
    path('<int:pk>/check-in/', views.appointment_check_in, name='check_in'),
    path('<int:pk>/cancel/', views.appointment_cancel, name='cancel'),
]

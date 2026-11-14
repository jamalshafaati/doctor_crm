from django.urls import path
from . import views
app_name = 'imaging'
urlpatterns = [
    path('', views.imaging_list, name='list'),
]

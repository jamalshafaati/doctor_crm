from django.urls import path
from . import views
app_name = 'public'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('book/', views.book, name='book'),
    path('contact/', views.contact, name='contact'),
]

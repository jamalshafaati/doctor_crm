from django.urls import path
from . import views
from . import settings_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', settings_views.clinic_settings, name='settings'),
]

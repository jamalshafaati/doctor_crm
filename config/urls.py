from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from apps.accounts.views import dashboard

urlpatterns = [
    path('i18n/setlang/', set_language, name='set_language'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    # Public marketing website (SEO)
    path('site/', include('apps.public.urls')),
]

urlpatterns += i18n_patterns(
    path('', dashboard, name='dashboard'),
    path('accounts/', include('apps.accounts.urls')),
    path('patients/', include('apps.patients.urls')),
    path('appointments/', include('apps.appointments.urls')),
    path('encounters/', include('apps.encounters.urls')),
    path('clinical/', include('apps.foot_ankle.urls')),
    path('diagnoses/', include('apps.diagnoses.urls')),
    path('imaging/', include('apps.imaging.urls')),
    path('treatment/', include('apps.treatment.urls')),
    path('prescriptions/', include('apps.prescriptions.urls')),
    path('surgery/', include('apps.surgery.urls')),
    path('followups/', include('apps.followups.urls')),
    path('medical-history/', include('apps.medical_history.urls')),
    path('portal/', include('apps.patient_portal.urls')),
    path('reports/', include('apps.reports.urls')),
    path('notifications/', include('apps.notifications.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib import admin
from .models import (
    TraumaExam, SportsExam, AchillesExam, FlatfootExam,
    DeformityExam, ArthritisExam, AnatomyFinding
)
for m in [TraumaExam, SportsExam, AchillesExam, FlatfootExam, DeformityExam, ArthritisExam, AnatomyFinding]:
    admin.site.register(m)

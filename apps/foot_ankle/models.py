"""
Specialized Foot & Ankle examination modules.
An Encounter can have multiple specialized assessments.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.clinical.models import Side


class TraumaExam(models.Model):
    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.CASCADE,
        related_name='trauma_exams', verbose_name=_('ویزیت')
    )
    injury_date = models.DateField(null=True, blank=True, verbose_name=_('تاریخ آسیب'))
    mechanism = models.TextField(blank=True, verbose_name=_('مکانیسم آسیب'))
    side = models.CharField(max_length=20, choices=Side.choices, default=Side.NA, verbose_name=_('طرف'))
    location = models.CharField(max_length=200, blank=True, verbose_name=_('محل آسیب'))
    weight_bearing = models.CharField(max_length=50, blank=True, verbose_name=_('تحمل وزن'))
    swelling = models.CharField(max_length=50, blank=True, verbose_name=_('تورم'))
    bruising = models.CharField(max_length=50, blank=True, verbose_name=_('کبودی'))
    deformity = models.CharField(max_length=100, blank=True, verbose_name=_('دفورمیتی'))
    tenderness = models.TextField(blank=True, verbose_name=_('حساسیت به لمس'))
    neurovascular_status = models.TextField(blank=True, verbose_name=_('وضعیت عصبی-عروقی'))
    imaging_findings = models.TextField(blank=True, verbose_name=_('یافته‌های تصویربرداری'))
    # Classifications
    weber_class = models.CharField(max_length=10, blank=True, verbose_name=_('طبقه‌بندی Weber'))
    lauge_hansen = models.CharField(max_length=50, blank=True, verbose_name=_('Lauge-Hansen'))
    ao_ota = models.CharField(max_length=50, blank=True, verbose_name=_('AO/OTA'))
    notes = models.TextField(blank=True, verbose_name=_('یادداشت'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('معاینه تروما')
        verbose_name_plural = _('معاینات تروما')


class SportsExam(models.Model):
    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.CASCADE,
        related_name='sports_exams', verbose_name=_('ویزیت')
    )
    sport_type = models.CharField(max_length=100, blank=True, verbose_name=_('نوع ورزش'))
    activity_level = models.CharField(max_length=50, blank=True, verbose_name=_('سطح فعالیت'))
    mechanism = models.TextField(blank=True, verbose_name=_('مکانیسم'))
    previous_injuries = models.TextField(blank=True, verbose_name=_('آسیب‌های قبلی'))
    side = models.CharField(max_length=20, choices=Side.choices, default=Side.NA, verbose_name=_('طرف'))
    instability = models.BooleanField(default=False, verbose_name=_('ناپایداری'))
    # Ligament tests
    atfl = models.CharField(max_length=50, blank=True, verbose_name=_('ATFL'))
    cfl = models.CharField(max_length=50, blank=True, verbose_name=_('CFL'))
    ptfl = models.CharField(max_length=50, blank=True, verbose_name=_('PTFL'))
    syndesmosis = models.CharField(max_length=50, blank=True, verbose_name=_('Syndesmosis'))
    anterior_drawer = models.CharField(max_length=50, blank=True, verbose_name=_('Anterior Drawer'))
    talar_tilt = models.CharField(max_length=50, blank=True, verbose_name=_('Talar Tilt'))
    squeeze_test = models.CharField(max_length=50, blank=True, verbose_name=_('Squeeze Test'))
    external_rotation_test = models.CharField(max_length=50, blank=True, verbose_name=_('External Rotation'))
    functional_tests = models.TextField(blank=True, verbose_name=_('تست‌های عملکردی'))
    return_to_sport = models.TextField(blank=True, verbose_name=_('ارزیابی بازگشت به ورزش'))
    notes = models.TextField(blank=True, verbose_name=_('یادداشت'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('معاینه ورزشی')
        verbose_name_plural = _('معاینات ورزشی')


class AchillesExam(models.Model):
    class ConditionType(models.TextChoices):
        ACUTE_RUPTURE = 'acute_rupture', _('پارگی حاد')
        TENDINOPATHY = 'tendinopathy', _('تاندینوپاتی')
        OTHER = 'other', _('سایر')

    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.CASCADE,
        related_name='achilles_exams', verbose_name=_('ویزیت')
    )
    condition_type = models.CharField(
        max_length=20, choices=ConditionType.choices, blank=True, verbose_name=_('نوع')
    )
    side = models.CharField(max_length=20, choices=Side.choices, default=Side.NA, verbose_name=_('طرف'))
    pain_location = models.CharField(max_length=100, blank=True, verbose_name=_('محل درد'))
    duration = models.CharField(max_length=100, blank=True, verbose_name=_('مدت'))
    tendon_tenderness = models.BooleanField(default=False, verbose_name=_('حساسیت تاندون'))
    tendon_thickening = models.BooleanField(default=False, verbose_name=_('ضخامت تاندون'))
    palpable_defect = models.BooleanField(default=False, verbose_name=_('نقص قابل لمس'))
    thompson_test = models.CharField(max_length=50, blank=True, verbose_name=_('تست Thompson'))
    single_leg_heel_raise = models.CharField(max_length=50, blank=True, verbose_name=_('Single-leg heel raise'))
    plantarflexion_strength = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name=_('قدرت پلانتارفلاکشن (MRC 0–5)')
    )
    imaging_findings = models.TextField(blank=True, verbose_name=_('یافته‌های US/MRI'))
    previous_treatment = models.TextField(blank=True, verbose_name=_('درمان قبلی'))
    notes = models.TextField(blank=True, verbose_name=_('یادداشت'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('معاینه آشیل')
        verbose_name_plural = _('معاینات آشیل')


class FlatfootExam(models.Model):
    class Flexibility(models.TextChoices):
        FLEXIBLE = 'flexible', _('انعطاف‌پذیر')
        RIGID = 'rigid', _('سفت')
        UNKNOWN = 'unknown', _('نامشخص')

    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.CASCADE,
        related_name='flatfoot_exams', verbose_name=_('ویزیت')
    )
    side = models.CharField(max_length=20, choices=Side.choices, default=Side.NA, verbose_name=_('طرف'))
    flexibility = models.CharField(
        max_length=20, choices=Flexibility.choices, default=Flexibility.UNKNOWN, verbose_name=_('انعطاف')
    )
    arch_height = models.CharField(max_length=50, blank=True, verbose_name=_('ارتفاع قوس'))
    hindfoot_alignment = models.CharField(max_length=50, blank=True, verbose_name=_('هم‌راستایی پاشنه'))
    forefoot_abduction = models.CharField(max_length=50, blank=True, verbose_name=_('ابداکشن جلوی پا'))
    heel_rise = models.CharField(max_length=50, blank=True, verbose_name=_('Heel rise'))
    jack_test = models.CharField(max_length=50, blank=True, verbose_name=_('Jack test'))
    single_heel_rise = models.CharField(max_length=50, blank=True, verbose_name=_('Single heel rise'))
    ptt_assessment = models.TextField(blank=True, verbose_name=_('ارزیابی تاندون تیبیال خلفی'))
    weight_bearing_xray = models.TextField(blank=True, verbose_name=_('یافته‌های X-ray تحمل وزن'))
    mearys_angle = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("زاویه Meary")
    )
    calcaneal_pitch = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_('Calcaneal pitch')
    )
    notes = models.TextField(blank=True, verbose_name=_('یادداشت'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('معاینه صافی کف پا')
        verbose_name_plural = _('معاینات صافی کف پا')


class DeformityExam(models.Model):
    class DeformityType(models.TextChoices):
        HALLUX_VALGUS = 'hallux_valgus', _('Hallux Valgus')
        HALLUX_RIGIDUS = 'hallux_rididus', _('Hallux Rigidus')
        HAMMERTOE = 'hammertoe', _('Hammertoe')
        CLAW_TOE = 'claw_toe', _('Claw Toe')
        CAVUS = 'cavus', _('Cavus Foot')
        FLATFOOT = 'flatfoot', _('Flatfoot')
        EQUINUS = 'equinus', _('Equinus')
        OTHER = 'other', _('سایر')

    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.CASCADE,
        related_name='deformity_exams', verbose_name=_('ویزیت')
    )
    deformity_type = models.CharField(
        max_length=30, choices=DeformityType.choices, verbose_name=_('نوع دفورمیتی')
    )
    side = models.CharField(max_length=20, choices=Side.choices, default=Side.NA, verbose_name=_('طرف'))
    location = models.CharField(max_length=100, blank=True, verbose_name=_('محل'))
    flexible_or_rigid = models.CharField(max_length=20, blank=True, verbose_name=_('انعطاف‌پذیر / سفت'))
    severity = models.CharField(max_length=50, blank=True, verbose_name=_('شدت'))
    progression = models.CharField(max_length=50, blank=True, verbose_name=_('پیشرفت'))
    functional_impact = models.TextField(blank=True, verbose_name=_('تأثیر عملکردی'))
    associated_deformities = models.TextField(blank=True, verbose_name=_('دفورمیتی‌های همراه'))
    imaging_measurements = models.TextField(blank=True, verbose_name=_('اندازه‌گیری‌های تصویربرداری'))
    notes = models.TextField(blank=True, verbose_name=_('یادداشت'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('معاینه دفورمیتی')
        verbose_name_plural = _('معاینات دفورمیتی')


class ArthritisExam(models.Model):
    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.CASCADE,
        related_name='arthritis_exams', verbose_name=_('ویزیت')
    )
    joint = models.CharField(max_length=100, blank=True, verbose_name=_('مفصل'))
    side = models.CharField(max_length=20, choices=Side.choices, default=Side.NA, verbose_name=_('طرف'))
    pain = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name=_('درد (۰–۱۰)')
    )
    stiffness = models.CharField(max_length=50, blank=True, verbose_name=_('خشکی'))
    morning_stiffness = models.CharField(max_length=50, blank=True, verbose_name=_('خشکی صبحگاهی'))
    swelling = models.CharField(max_length=50, blank=True, verbose_name=_('تورم'))
    rom = models.TextField(blank=True, verbose_name=_('دامنه حرکتی'))
    functional_limitation = models.TextField(blank=True, verbose_name=_('محدودیت عملکردی'))
    imaging_findings = models.TextField(blank=True, verbose_name=_('یافته‌های تصویربرداری'))
    takakura_stage = models.CharField(max_length=10, blank=True, verbose_name=_('مرحله Takakura'))
    notes = models.TextField(blank=True, verbose_name=_('یادداشت'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('معاینه آرتریت')
        verbose_name_plural = _('معاینات آرتریت')


class AnatomyFinding(models.Model):
    """
    Interactive foot anatomy markers.
    Stores region + side + finding type + optional normalized coordinates.
    """
    class FindingType(models.TextChoices):
        PAIN = 'pain', _('درد')
        TENDERNESS = 'tenderness', _('حساسیت')
        SWELLING = 'swelling', _('تورم')
        DEFORMITY = 'deformity', _('دفورمیتی')
        NUMBNESS = 'numbness', _('بی‌حسی')
        OTHER = 'other', _('سایر')

    class View(models.TextChoices):
        DORSAL = 'dorsal', _('پشتی (Dorsal)')
        PLANTAR = 'plantar', _('کفی (Plantar)')
        LATERAL = 'lateral', _('جانبی (Lateral)')

    encounter = models.ForeignKey(
        'encounters.Encounter', on_delete=models.CASCADE,
        related_name='anatomy_findings', verbose_name=_('ویزیت')
    )
    view = models.CharField(max_length=20, choices=View.choices, verbose_name=_('نما'))
    region = models.CharField(max_length=100, verbose_name=_('ناحیه آناتومیک'))
    side = models.CharField(max_length=20, choices=Side.choices, default=Side.NA, verbose_name=_('طرف'))
    finding_type = models.CharField(max_length=20, choices=FindingType.choices, verbose_name=_('نوع یافته'))
    severity = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('شدت (۱–۵)')
    )
    notes = models.TextField(blank=True, verbose_name=_('یادداشت'))
    # Normalized coordinates (0–1) for marker placement on illustration
    coord_x = models.FloatField(null=True, blank=True, verbose_name=_('مختصات X'))
    coord_y = models.FloatField(null=True, blank=True, verbose_name=_('مختصات Y'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('یافته آناتومیک')
        verbose_name_plural = _('یافته‌های آناتومیک')
        ordering = ['view', 'region']

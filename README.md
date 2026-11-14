<<<<<<< HEAD
# کلینیک تخصصی پا و مچ پا — سیستم مدیریت و EMR

**Foot & Ankle Specialist Clinic Management & EMR**

سیستم مدیریت کلینیک تخصصی پا و مچ پا | Modular Monolith | Django 6

---

## وضعیت فعلی پروژه

| فاز | عنوان | وضعیت |
|-----|--------|--------|
| ۱ | معماری، ERD، Design System | ✅ |
| ۲ | Foundation (User، RTL/LTR، Design Tokens) | ✅ |
| ۳ | Application Shell + داشبوردهای نقش‌محور | ✅ |
| ۴ | بیماران + نوبت‌دهی + چک‌این + Encounter + سابقه پزشکی | ✅ |
| ۵ | معاینات تخصصی + آناتومی + تشخیص + تصویربرداری + نسخه | ✅ |
| ۶ | جراحی + پیگیری | ✅ |
| ۷ | پورتال بیمار + گزارش‌ها + اعلان‌ها | ✅ |
| ۸ | تست، امنیت، Production | ⏳ |

---

## تکنولوژی‌ها

- **Backend:** Python 3.12+ / Django 6.1
- **Database:** SQLite (توسعه) — قابل مهاجرت به PostgreSQL
- **Frontend:** Django Templates + HTMX + Alpine.js
- **UI:** CSS Design System اختصاصی (بدون Bootstrap)
- **زبان:** فارسی (RTL) پیش‌فرض + انگلیسی (LTR)
- **تاریخ:** ذخیره میلادی در دیتابیس — نمایش شمسی/میلادی بر اساس زبان

---

## ساختار پروژه

```
clinic/
├── config/                  # تنظیمات Django
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── accounts/            # کاربر سفارشی، نقش‌ها، پروفایل‌ها، تنظیمات کلینیک
│   ├── patients/            # مدیریت بیماران
│   ├── appointments/        # نوبت‌دهی و چک‌این
│   ├── encounters/          # ویزیت بالینی + اصلاحات
│   ├── medical_history/     # سابقه پزشکی، آلرژی، هشدار
│   ├── clinical/            # معاینه عمومی (فاز ۵)
│   ├── foot_ankle/          # معاینات تخصصی پا و مچ پا (فاز ۵)
│   ├── diagnoses/           # تشخیص‌ها (فاز ۵)
│   ├── imaging/             # تصویربرداری (فاز ۵)
│   ├── documents/           # اسناد پزشکی
│   ├── treatment/           # طرح درمان
│   ├── prescriptions/       # نسخه
│   ├── surgery/             # جراحی
│   ├── followups/           # پیگیری
│   ├── patient_portal/      # پورتال بیمار
│   ├── notifications/       # اعلان‌ها
│   ├── reports/             # گزارش و آمار
│   └── audit/               # لاگ ممیزی
├── templates/
│   ├── base/
│   ├── components/          # Sidebar, Topbar, ...
│   ├── layouts/
│   ├── accounts/
│   ├── dashboard/
│   ├── patients/
│   └── appointments/
├── static/
│   ├── css/main.css         # Design System
│   ├── js/
│   └── fonts/
├── requirements/
├── locale/
├── media/
├── manage.py
└── README.md
```

---

## نصب و راه‌اندازی

### پیش‌نیاز
- Python 3.12+
- pip

### مراحل

```bash
# ۱. استخراج و ورود به پوشه پروژه
cd clinic-emr   # یا نام پوشه استخراج‌شده

# ۲. ایجاد محیط مجازی (توصیه می‌شود)
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# ۳. نصب وابستگی‌ها
pip install -r requirements/base.txt
# در صورت نیاز:
pip install Django djangorestframework django-htmx django-filter drf-spectacular Pillow python-dotenv

# ۴. تنظیمات محیطی
cp .env.example .env
# در صورت تمایل DJANGO_SECRET_KEY را تغییر دهید

# ۵. مایگریشن
python manage.py migrate

# ۶. ایجاد کاربر ادمین (در صورت نیاز)
python manage.py createsuperuser
# یا از کاربران آماده زیر استفاده کنید

# ۷. اجرای سرور
python manage.py runserver
```

سپس به آدرس زیر بروید:  
**http://127.0.0.1:8000/**

---

## حساب‌های آزمایشی

| نقش | نام کاربری | رمز عبور |
|-----|------------|----------|
| مدیر سیستم | `admin` | `admin123` |
| پزشک | `doctor` | `doctor123` |
| پذیرش | `reception` | `reception123` |

> **توجه:** در محیط واقعی حتماً رمزها را تغییر دهید.

---

## قابلیت‌های پیاده‌سازی‌شده تا فاز ۴

### احراز هویت و نقش‌ها
- مدل کاربر سفارشی با نقش‌های: پزشک، پذیرش، بیمار، ادمین
- پروفایل پزشک و پرسنل
- ورود / خروج
- منوی سایدبار وابسته به نقش

### بیماران
- ثبت بیمار با شماره پرونده خودکار (`P-YYYYMMDD-XXXX`)
- جستجوی پیشرفته (نام، شماره پرونده، تلفن، کد ملی)
- پروفایل بیمار + آلرژی + هشدار بالینی
- ویرایش اطلاعات دموگرافیک

### نوبت‌دهی
- رزرو نوبت
- جلوگیری از تداخل زمانی (double-booking) برای یک پزشک
- وضعیت‌ها: Scheduled / Confirmed / Checked-in / Completed / Cancelled / No-show
- چک‌این بیمار
- لغو نوبت
- فیلتر بر اساس تاریخ و وضعیت

### ویزیت (Encounter)
- ایجاد از نوبت یا walk-in
- وضعیت‌های Draft → In Progress → Pending Review → Finalized → Amended
- قفل شدن پس از نهایی‌سازی
- مدل اصلاح کنترل‌شده (Amendment) با دلیل و تاریخچه

### سابقه پزشکی
- سابقه پزشکی / جراحی / دارویی / خانوادگی / اجتماعی
- آلرژی با شدت
- هشدار بالینی

### رابط کاربری
- Design System پریمیوم (رنگ‌های Navy/Teal)
- پشتیبانی کامل RTL (فارسی) و LTR (انگلیسی)
- تغییر زبان از تاپ‌بار
- داشبورد جداگانه پزشک و پذیرش
- Empty state و Loading آماده

---

## تنظیمات دیتابیس

در حال حاضر از **SQLite** استفاده می‌شود (مناسب توسعه).

برای PostgreSQL در production، در `config/settings/production.py` بخش DATABASES را فعال کنید:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

---

## قوانین مهم معماری

1. منطق کسب‌وکار داخل `services/` است — نه داخل ویوها.
2. دسترسی‌ها در بک‌اند enforce می‌شوند (نه فقط مخفی‌کردن دکمه).
3. فایل‌های پزشکی هرگز با URL عمومی سرو نمی‌شوند.
4. ویزیت نهایی‌شده silently overwrite نمی‌شود.
5. تاریخ‌ها در دیتابیس میلادی ذخیره می‌شوند.

---

## فازهای بعدی (برنامه)

- **فاز ۵:** معاینه عمومی و تخصصی پا/مچ پا، آناتومی تعاملی، تشخیص، تصویربرداری امن، طرح درمان، نسخه
- **فاز ۶:** جراحی، ایمپلنت، دستورات بعد از عمل، پیگیری
- **فاز ۷:** پورتال بیمار، انتشار اسناد، اعلان‌ها، گزارش و آمار واقعی
- **فاز ۸:** تست خودکار، سخت‌سازی امنیتی، مستندات Deployment و Backup

---

## مجوز

این پروژه برای استفاده کلینیکی تخصصی طراحی شده است.  
قبل از استفاده در محیط واقعی، ارزیابی امنیتی و انطباق با مقررات محلی (از جمله حریم خصوصی داده‌های پزشکی) ضروری است.

---

**نسخه:** 0.7.1 (تا پایان فاز ۷)  
**آخرین به‌روزرسانی:** نوامبر ۲۰۲۶
=======
# doctor_crm
>>>>>>> 8bece008f73d6b48680ba5310d9a9c9909beb585

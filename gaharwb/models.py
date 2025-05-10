from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models import Count
import django_jalali.db.models as jmodels
import datetime
from django.utils import timezone




class Specialty(models.Model):
    name=models.CharField(max_length=50 , unique=True , verbose_name="عنوان تخصص")

    class Meta:
        verbose_name= "تخصص"
        verbose_name_plural= "تخصص ها"


    def __str__(self):
        return self.name






class Member(models.Model):

    ROLE_CHOICES=[
        ('leader' , 'سرپرست تیم'),
        ('advisor' , 'مشاور تیم'),
        ('member' , 'عضو تیم')
    ]

    fname=models.CharField(max_length=40 , blank=False , null=True , verbose_name="نام")
    lname=models.CharField(max_length=40 , blank=False , null=True, verbose_name="نام خانوادگی")
    email=models.EmailField(null=True , blank=True, verbose_name="ایمیل")
    description=models.TextField(null=True , blank=True , verbose_name="توضیحات")
    phone_number = PhoneNumberField(
        region="IR",
        unique=True,
        verbose_name="شماره تماس" ,
        validators=[
            RegexValidator(
                regex=r"^(\+98|0)9\d{9}$",
                message="شماره تلفن باید 11 رقمی باشد و با 98 شروع شود."
            )
        ],

    )
    national_code = models.CharField(
        max_length=10,  # حداکثر 10 رقم
        unique=True,  # یونیک بودن کد ملی
        verbose_name="کدملی",
        validators=[  # می‌توانیم از یک ولیداتور برای تایید رقم بودن استفاده کنیم
            RegexValidator(
                regex=r'^\d{10}$',  # فقط 10 رقم مجاز است
                message="کد ملی باید شامل 10 رقم باشد."
            )
        ]
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE , verbose_name="اکانت")
    resume=models.FileField(upload_to='media/resumes/',null=True , blank=True, verbose_name="رزومه")
    image=models.ImageField(upload_to='media/images/',null=True , blank=True, verbose_name="تصویر")
    role=models.CharField(max_length=7 , choices=ROLE_CHOICES , default='member', verbose_name="نقش")
    team=models.ForeignKey('Team', on_delete=models.CASCADE , related_name='members', verbose_name="نام تیم")
    specialties=models.ManyToManyField('Specialty', verbose_name="تخصص ها")


    class Meta:
        verbose_name= "عضو تیم"
        verbose_name_plural= "اعضای تیم"
        unique_together = ('fname' , 'lname')
        ordering = ('fname' , 'lname' , 'role' , 'team')


    def __str__(self):
        return f"{self.fname} {self.lname}"






class Team(models.Model):
    LEVEL_CHOICES=[
        ('beginner' , 'مبتدی'),
        ('intermediate' , 'متوسط'),
        ('expert' , 'حرفه ای')
    ]
    name=models.CharField(max_length=60 , unique=True , null=False , blank=False, verbose_name="نام تیم")
    specialties = models.ManyToManyField('Specialty', related_name='teams', verbose_name="تخصص ها")
    description = models.TextField(blank = False , null= True ,verbose_name= "توضیحات")
    level=models.CharField(choices=LEVEL_CHOICES , max_length=12 , verbose_name="سطح تیم", default='beginner')


    class Meta:
        verbose_name= "تیم"
        verbose_name_plural= "تیم ها"


    def __str__(self):
        return self.name

    @classmethod
    def ordered_teams(cls):
        return cls.objects.annotate(specialty_count=Count('specialties')).order_by('-specialty_count', 'name')




class Project(models.Model):

    STATUS_CHOICES = [
        ('DONE' , 'خاتمه یافته'),
        ('IN_PROGRESS' , 'در حال انجام'),
        ('Available' , 'در دسترس')
    ]

    title = models.CharField(max_length=100 , blank=False , null=False , unique=True, verbose_name="عنوان پروژه")
    description=models.TextField( verbose_name="توضیحات")
    publish_date = jmodels.jDateField(verbose_name="تاریخ انتشار", auto_now_add=True)
    status=models.CharField(max_length=11 , choices=STATUS_CHOICES , default='Available', verbose_name="وضعیت پروژه")
    functor=models.ForeignKey('Team' , null=True , blank=True , on_delete=models.SET_NULL , related_name='projects', verbose_name="نام تیم")
    requested_teams = models.ManyToManyField('Team', related_name='requested_projects' , blank=True , null=True ,verbose_name="تیم های متقاضی")
    rfp=models.FileField(upload_to='media/rfps/' , null=True , blank=True, verbose_name="فایل نیاز تفضیلی")

    class Meta:
        verbose_name= "پروژه"
        verbose_name_plural= "پروژه ها"
        ordering = ('title' , 'status' , 'publish_date')

    def __str__(self):
        return self.title




class Request_for_Collaboration(models.Model):
    fname=models.CharField(max_length=50 , null=False , blank=False, verbose_name= "نام" )
    lname=models.CharField(max_length=50 , null=False , blank=False, verbose_name= "نام خانوادگی" )
    email = models.EmailField(null=True, blank=False, verbose_name= "ایمیل" )
    phone_number = PhoneNumberField(
        region="IR",
        unique=True,
        verbose_name="شماره تماس" ,
        validators=[
            RegexValidator(
                regex=r"^(\+98|0)9\d{9}$",
                message="شماره تلفن باید 11 رقمی باشد و با 98 یا 0 شروع شود."
            )
        ],


    )
    resume = models.FileField(upload_to='media/requests/', null=True, blank=True, verbose_name="رزومه")
    specialties = models.ManyToManyField('Specialty', verbose_name="تخصص ها")
    description = models.TextField(verbose_name="توضیحات" ,  blank=True , null=True)
    otp_code = models.CharField(max_length=6 , null=True , blank=False)
    otp_created_at = models.DateTimeField(blank=True , null=True)
    is_verified = models.BooleanField(default=False)

    def is_otp_valid(self):
        if not self.otp_created_at:
            return False
        return timezone.now() < self.otp_created_at + datetime.timedelta(minutes=5)

    class Meta:
        verbose_name= "درخواست همکاری"
        verbose_name_plural= "درخواست های همکاری"
        unique_together = ('fname' , 'lname')



    def __str__(self):
        return f"{self.fname} {self.lname}"

    @classmethod
    def ordered_requests(cls):
        return cls.objects.annotate(specialty_count=Count('specialties')).order_by('-specialty_count', 'name')

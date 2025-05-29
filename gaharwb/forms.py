from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Request_for_Collaboration, Specialty
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
import re


class RequestCollaborationForm(forms.ModelForm):
    specialties = forms.ModelMultipleChoiceField(
        queryset=Specialty.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Request_for_Collaboration
        fields = ['fname', 'lname', 'phone_number', 'email', 'resume', 'specialties', 'description']

        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-input w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'message': forms.Textarea(attrs={'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400', 'rows': 4}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # استفاده از regex برای اعتبارسنجی ایمیل
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("لطفاً ایمیل صحیح وارد کنید.")
        return email

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        # بررسی نوع فایل رزومه
        if resume:
            file_type = resume.content_type
            allowed_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
            if file_type not in allowed_types:
                raise ValidationError("فقط فایل‌های PDF و Word مجاز هستند.")
        return resume


class LoginForm(forms.Form):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'})
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'})
    )
    captcha = CaptchaField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # جلوگیری از حملات XSS
        if '<' in username or '>' in username:
            raise ValidationError("نام کاربری حاوی کاراکترهای نامعتبر است.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # جلوگیری از تزریق داده (در اینجا برای رمز عبور)
        if ';' in password or '--' in password:
            raise ValidationError("رمز عبور حاوی کاراکترهای نامعتبر است.")
        return password

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Request_for_Collaboration , Specialty
from captcha.fields import CaptchaField


class RequestCollaborationForm(forms.ModelForm):
    specialties = forms.ModelMultipleChoiceField(
        queryset=Specialty.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Request_for_Collaboration
        fields = ['fname', 'lname', 'phone_number', 'email','resume', 'specialties', 'description' , ]

        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'phone': forms.TextInput(attrs={'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-input w-full border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'message': forms.Textarea(attrs={'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400', 'rows': 4}),
        }

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
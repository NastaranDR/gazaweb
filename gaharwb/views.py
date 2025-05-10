from django.shortcuts import render, redirect , get_object_or_404 , get_list_or_404
from django.contrib.auth import authenticate, login
from .forms import RequestCollaborationForm, LoginForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import Http404 , HttpResponse
import random
from django.core.mail import send_mail
from django.utils import timezone
from dotenv import load_dotenv
from django.conf import settings
import environ
from django.views.generic import TemplateView


load_dotenv()

def home(request):
    teams=Team.objects.all()
    experts=teams.filter(level="expert")
    intermediates=teams.filter(level="intermediate")
    beginners=teams.filter(level="beginner")
    context={
        "teams":teams,
        "experts":experts,
        "intermediates":intermediates,
        "beginners":beginners
    }
    return render(request, 'home.html' , context)

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, otp_code):
    subject = 'کد تایید درخواست همکاری'
    message = f'کد تایید شما: {otp_code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to_email]
    send_mail(subject, message, email_from, recipient_list)

def request_collaboration(request):
    if request.method == "POST":
        form = RequestCollaborationForm(request.POST, request.FILES)
        if form.is_valid():
            collab = form.save(commit=False)
            otp = generate_otp()
            collab.otp_code = otp
            collab.otp_created_at = timezone.now()
            collab.save()
            send_otp_email(collab.email, otp)
            return redirect('verify_otp', collab_id=collab.id)
    else:
        form = RequestCollaborationForm()

    return render(request, 'request_collaboration.html', {'form': form ,})


def verify_otp_view(request, collab_id):
    collab = get_object_or_404(Request_for_Collaboration , id=collab_id)
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if collab.is_otp_valid() and entered_otp == collab.otp_code:
            collab.is_verified = True
            collab.save()
            return redirect('request_thank_you')
        else:
            return HttpResponse('کد اشتباه است یا منقضی شده است.')

    return render(request, 'verify_otp.html', {'collab': collab})



def request_thank_you(request):
    return render(request, 'request_thank_you.html')

def login_view(request):

        if request.user.is_authenticated:
            return redirect('profile')
        next_url = request.GET.get('next') or request.POST.get('next') or 'profile'
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('profile')
                else:
                    form.add_error(None, "نام کاربری یا رمز عبور اشتباه است")
        else:
            form = LoginForm()

        return render(request, 'login.html', {'form': form , 'next': next_url})

@login_required
def profile(request):
    user = request.user
    member=get_object_or_404(Member , user=user)
    projects=Project.objects.filter(status='Available')
    context={
        'user':user,
        'member':member,
        'team':member.team.name,
        'projects':projects,
        'role':member.get_role_display()
    }
    return render(request, 'profile.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': project})

def contact(request):
    return render(request, 'contact.html')

def team_members(request):
    user=request.user
    member=get_object_or_404(Member , user=user)
    try:
        team=member.team
        members=team.members.all()
    except team.DoesNotExist:
        raise Http404('تیم یافت نشد')

    context={
        'members':members ,
        'team' : team,
    }

    return render(request, 'team_members.html' , context)




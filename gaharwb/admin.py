from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django import forms
from django.contrib import admin
import jdatetime


admin.site.site_header = "داشبورد مدیریت سایت گهر"
admin.site.site_title = "مدیریت سایت"
admin.site.index_title = "به داشبورد مدیریت خوش آمدید"



@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'phone_number', 'email', 'role', 'team')
    list_filter = ('role', 'team', 'specialties')
    search_fields = ('fname', 'lname', 'email', 'phone_number', 'national_code')
    ordering = ('fname', 'lname', 'role', 'team')
    autocomplete_fields = ('specialties', 'team', 'user')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'Specialties')
    filter_horizontal = ('specialties',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'publish_date', 'functor')
    list_filter = ('status', 'functor', 'requested_teams')
    search_fields = ('title', 'description')
    ordering = ('title', 'status', 'publish_date')
    date_hierarchy = 'publish_date'
    filter_horizontal = ('requested_teams',)
    # def get_publish_date(self, obj):
    #     return jdatetime.date.fromgregorian(date=obj.publish_date)  # تبدیل به شمسی
    # get_publish_date.short_description = "تاریخ انتشار (شمسی)"


@admin.register(Request_for_Collaboration)
class RequestForCollaborationAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'phone_number', 'email')
    search_fields = ('fname', 'lname', 'email', 'phone_number')
    filter_horizontal = ('specialties',)





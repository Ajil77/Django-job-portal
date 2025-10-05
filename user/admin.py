from django.contrib import admin
from .models import User, JobSeekerProfile, EmployerProfile, Job, Application

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'created_at')
    list_filter = ('role',)

@admin.register(JobSeekerProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'education', 'experience')

@admin.register(EmployerProfile)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'website')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'salary', 'created_at')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'jobseeker', 'status', 'applied_at')

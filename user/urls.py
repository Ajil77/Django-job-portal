from django.urls import path
from . import views

urlpatterns = [
    path('',views.register, name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view,name='logout'),

    
    path('jobseeker/',views.jobseeker_home, name='jobseeker_home'),
    path('employer/',views.employer_home, name= 'employer_home'),
    path('admin_home/',views.admin_home, name='admin_home'),



    path('post_job/',views.post_job, name='post_job'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),



        path('employer-profile/', views.employer_profile, name='employer_profile'),
        path('job-search/', views.search_jobs, name='job_search'),
        path('jobseeker-profile/', views.jobseeker_profile, name='jobseeker_profile'),
        path('jobseeker-view-profile/', views.jobseeker_view_profile, name='jobseeker_view_profile'),
        path('job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
         path('job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
]

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User, JobSeekerProfile , EmployerProfile, Job, Application


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role', 'jobseeker')

        # Allow only one admin
        if role == 'admin' and User.objects.filter(role='admin').exists():
            messages.error(request, "Admin already exists. Only one admin allowed.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role=role
        )
        messages.success(request, "Account created successfully")
        return redirect('login')

    
    return render(request, 'register.html')
    

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            # ✅ Check hashed password
            if check_password(password, user.password):
                # Save session
                request.session['user_id'] = user.id
                request.session['user_role'] = user.role

                # Redirect based on role
                if user.role == 'jobseeker':
                    return redirect('jobseeker_home')
                elif user.role == 'employer':
                    return redirect('employer_home')
                else:
                    return redirect('admin_home')
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, 'login.html')









def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect("login")



def jobseeker_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    profile = JobSeekerProfile.objects.filter(user=user).first()
    applications_count = Application.objects.filter(jobseeker=user).count()
    recommended_jobs = Job.objects.all().order_by('-id')[:5]
    context = {
        'user': user,
        'profile': profile,
        'applications_count': applications_count,
        'recommended_jobs': recommended_jobs
    }
    return render(request, 'jobseeker_home.html', context)


def jobseeker_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    profile, created = JobSeekerProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile.skills = request.POST.get('skills')
        profile.education = request.POST.get('education')
        profile.experience = request.POST.get('experience')
        profile.contact_number = request.POST.get('contact_number')
        if request.FILES.get('resume'):
            profile.resume = request.FILES['resume']
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('jobseeker_home')

    context = {'user': user, 'profile': profile}
    return render(request, 'jobseeker_profile.html', context)


def employer_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    profile = EmployerProfile.objects.filter(user=user).first()
    jobs = Job.objects.filter(employer=user)
    context = {'user': user, 'profile': profile, 'jobs': jobs}
    return render(request, 'employer_home.html', context)






def admin_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    if user.role != 'admin':  
        return redirect('login')

 
    total_users = User.objects.count()
    total_jobs = Job.objects.count()
    total_applications = Application.objects.count()

   
    recent_jobs = Job.objects.all().order_by('-id')[:5]
    recent_applications = Application.objects.all().order_by('-id')[:5]

    context = {
        'total_users': total_users,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'recent_jobs': recent_jobs,
        'recent_applications': recent_applications,
        'all_users': User.objects.all(),   # if you want full list
        'all_jobs': Job.objects.all(),
        'all_applications': Application.objects.all(),
    }
    return render(request, 'admin_home.html', context)



def post_job(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        salary = request.POST.get('salary')

        Job.objects.create(
            employer=user,
            title=title,
            description=description,
            location=location,
            salary=salary
        )
        messages.success(request, "Job posted successfully!")
        return redirect('employer_home')

    return render(request, 'post_job.html')


def apply_job(request, job_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    job = Job.objects.get(id=job_id)


    if Application.objects.filter(jobseeker=user, job=job).exists():
        messages.warning(request, "You already applied for this job.")
    else:
        Application.objects.create(job=job, jobseeker=user, status='pending')
        messages.success(request, "Application submitted successfully!")

    return redirect('jobseeker_home')


def employer_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = User.objects.get(id=user_id)
    profile, created = EmployerProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        profile.company_name = request.POST.get('company_name')
        profile.company_description = request.POST.get('company_description')
        profile.website = request.POST.get('website')
        profile.contact_number = request.POST.get('contact_number')
        if request.FILES.get('logo'):
            profile.logo = request.FILES['logo']
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('employer_home')

    context = {'profile': profile, 'user': user}
    return render(request, 'employer_profile.html', context)



def search_jobs(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    query = request.GET.get('query', '')
    jobs = Job.objects.filter(title__icontains=query) if query else Job.objects.all()

    context = {'jobs': jobs, 'query': query}
    return render(request, 'job_search.html', context)


def jobseeker_view_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    profile = JobSeekerProfile.objects.filter(user=user).first()

    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'jobseeker_view_profile.html', context)
def view_applicants(request, job_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    
    # Only employer can view applicants
    if user.role != 'employer':
        return redirect('login')
    
    job = get_object_or_404(Job, id=job_id, employer=user)
    applicants = Application.objects.filter(job=job).order_by('-id')

    context = {
        'job': job,
        'applicants': applicants
    }
    return render(request, 'view_applicants.html', context)



def delete_job(request, job_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)

    if user.role != 'employer':
        messages.error(request, "Unauthorized access")
        return redirect('login')

    job = get_object_or_404(Job, id=job_id, employer=user)
    job.delete()
    messages.success(request, "Job deleted successfully")
    return redirect('employer_home')
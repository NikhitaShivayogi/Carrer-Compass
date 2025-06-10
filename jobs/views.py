from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages  # <-- added
from .forms import CustomUserCreationForm, ApplicationForm, UserProfileForm, UserUpdateForm
from .models import Job, Company, Application, UserProfile
from django.conf import settings


def home(request):
    
    if request.user.is_authenticated:
        return redirect('user_home')  # Redirect to user's personalized homepage
    return render(request, 'jobs/home.html', {
        'MEDIA_URL': settings.MEDIA_URL,
    })


@login_required
def user_home(request):
    return render(request, 'jobs/user_home.html', {
        'user': request.user,
        'MEDIA_URL': settings.MEDIA_URL,
    })


def job_list(request):
    jobs = Job.objects.all().order_by('-posted_date')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = job.applications.filter(user=request.user).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            resume = request.FILES.get('resume')
            # Validate resume format
            if resume and not resume.name.endswith(('.pdf', '.docx')):
                messages.error(request, "Invalid resume format. Please upload PDF or DOCX.")
            else:
                application = form.save(commit=False)
                application.job = job
                application.user = request.user
                application.save()
                messages.success(request, "Application submitted successfully!")
                return redirect('job_detail', job_id=job.id)
        else:
            messages.error(request, "There was an error with your application. Please check the form.")
    else:
        form = ApplicationForm()

    context = {
        'job': job,
        'form': form,
        'has_applied': has_applied,
    }
    return render(request, 'jobs/job_detail.html', context)


def company_profile(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    jobs = company.jobs.all()
    return render(request, 'jobs/company_profile.html', {'company': company, 'jobs': jobs})


@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'jobs/user_profile.html', {'profile': profile})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful! You are now logged in.")
            return redirect('user_home')
        else:
            messages.error(request, "Signup failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'jobs/signup.html', {'form': form})


@login_required
def edit_profile(request):
    # Form for updating built-in User fields
    user_form = UserUpdateForm(request.POST or None, instance=request.user)

    # Form for updating extended profile fields
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile_form = UserProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

    return render(request, 'jobs/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,  # ✅ pass this to access profile.profile_picture
        'user': request.user,
    })


@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).select_related('job', 'job__company')
    context = {
        'applications': applications,
    }
    return render(request, 'jobs/my_applications.html', context)

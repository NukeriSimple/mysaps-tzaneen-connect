from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from .forms import UserRegistrationForm, UserProfileForm, PhoneNumberRegistrationForm
from .models import CustomUser

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, _('Registration successful! Welcome to MySAPS Tzaneen Connect.'))
            return redirect('cases:dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def phone_register(request):
    """Phone number only registration"""
    if request.method == 'POST':
        form = PhoneNumberRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            phone = form.cleaned_data['phone_number']
            temp_password = phone[-6:]
            
            user = CustomUser.objects.create_user(
                username=username,
                phone_number=phone,
                password=temp_password
            )
            user.first_name = username
            user.save()
            
            login(request, user)
            messages.success(request, _('Registration successful! Please update your profile.'))
            return redirect('accounts:profile')
    else:
        form = PhoneNumberRegistrationForm()
    
    return render(request, 'accounts/phone_register.html', {'form': form})

def user_login(request):
    """Login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            if user.preferred_language:
                request.session['django_language'] = user.preferred_language
            messages.success(request, _('Welcome back!'))
            return redirect('cases:dashboard')
        else:
            messages.error(request, _('Invalid username or password.'))
    
    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            request.session['django_language'] = request.user.preferred_language
            messages.success(request, _('Profile updated successfully!'))
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect('home')
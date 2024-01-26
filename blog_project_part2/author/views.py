from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post

def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        register_form = forms.RegistrationForm()
            
    return render(request, 'user_form.html', {'form': register_form, 'type':'Register'})

def user_login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            user_password = login_form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                messages.success(request, 'Logged in successfully')
                login(request, user)
                return redirect('home')
            # else:
            #     messages.warning(request, 'Login informations are incorrect')    
            #     return redirect('login')   
        else:
            messages.info(request, 'Login informations are incorrect')
            return redirect('login')        
    else:
        login_form = AuthenticationForm()
        return render(request, 'user_form.html', {'form': login_form, 'type':'Login'})

@login_required
def profile(request):
    data = Post.objects.filter(author = request.user)
    return render(request, 'profile.html', {'data' : data})

@login_required   
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance = request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        profile_form = forms.ChangeUserForm(instance = request.user)
            
    return render(request, 'user_form.html', {'form': profile_form, 'type':'Edit Profile'})

@login_required
def pass_change(request):
    if request.method == 'POST':
        pass_change_form = PasswordChangeForm(request.user, data=request.POST)
        if pass_change_form.is_valid():
            pass_change_form.save()
            messages.success(request, 'Password updated successfully')
            update_session_auth_hash(request, pass_change_form.user)
            return redirect('profile')
    else:
        pass_change_form = PasswordChangeForm(user=request.user)
            
    return render(request, 'pass_change.html', {'form': pass_change_form, 'type':'Register'})

@login_required
def user_logout(request):
    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect('login')
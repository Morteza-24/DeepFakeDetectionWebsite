from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth import get_user_model
from .forms import SignUpForm, CustomAuthenticationForm, UserUpdateForm
# from django.db.models import Q

def home_view(request):
    return render(request, 'users/index.html', {"is_logged_in": request.user.is_authenticated})

def signin_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"خوش آمدید {user.first_name}!")
                return redirect('home')
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "ثبت‌نام با موفقیت انجام شد!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل شما با موفقیت به‌روزرسانی شد.")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'user/profile_edit.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "شما با موفقیت از حساب کاربری خارج شدید.")
    return redirect('home')
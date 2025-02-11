from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .forms import SignUpForm, CustomAuthenticationForm, UserUpdateForm, CustomPasswordResetForm, CustomSetPasswordForm
# from django.db.models import Q
from django.utils.translation import gettext as gt
from django.utils.translation import gettext_lazy as gt_l

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

# from django.conf import settings
# from django.utils import translation
# from django.urls import reverse

# def set_language_view(request):
#     language = request.GET.get('language', settings.LANGUAGE_CODE)

#     if language in dict(settings.LANGUAGES).keys():
#         translation.activate(language)
#         request.session[translation.LANGUAGE_SESSION_KEY] = language

#     return_path = request.META.get('HTTP_REFERER', reverse('home'))
#     return redirect(return_path)


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
                messages.success(
                    request, (gt("خوش آمدید %(name)s!") % {'name': user.first_name}))
                re = request.GET.get("next")
                return redirect(re if re else 'home')
            else:
                messages.error(request, gt_l("نام کاربری یا رمز عبور اشتباه است."))
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, gt_l("ثبت‌نام با موفقیت انجام شد!"))
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def profile_view(request):
    user_images = request.user.uploaded_images.all().order_by('-upload_date')
    user_videos = request.user.uploaded_videos.all().order_by('-upload_date')
    return render(request, 'users/profile.html', {
        'user': request.user,
        'images': user_images,
        'videos': user_videos
    })


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES,
                              instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, gt_l("پروفایل شما با موفقیت به‌روزرسانی شد."))
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'user/profile_edit.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, gt_l("شما با موفقیت از حساب کاربری خارج شدید."))
    return redirect('home')

def password_reset_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email)
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            
            email_context = {
                'user': user,
                'reset_url': reset_url,
                'site_name': 'Hatef'  
            }
            email_body = render_to_string('users/password_reset_email.html', email_context)
            email_subject = gt("سلام %(name)s! این ایمیل توسط سایت %(site_name)s به دلیل درخواست شما برای تغییر رمز عبور ارسال شده است.")% {'name': user.first_name, 'site_name': email_context['site_name']}

            
            send_mail(  
                email_subject,
                email_body,
                None,  # From email (will use DEFAULT_FROM_EMAIL from settings)
                [user.email],
                fail_silently=False,
            )
            
            messages.info(request, gt_l('اگر ایمیل وارد شده در سیستم موجود باشد، '
                                   'دستورالعمل‌های بازنشانی رمز عبور برای شما ارسال خواهد شد.'))
            return redirect('password_reset_done')
    else:
        form = CustomPasswordResetForm()
    
    return render(request, 'users/password_reset.html', {'form': form})

def password_reset_done_view(request):

    return render(request, 'users/password_reset_done.html')

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        
        if not default_token_generator.check_token(user, token):
            messages.error(request, gt_l('لینک بازنشانی رمز عبور نامعتبر است.'))
            return redirect('password_reset')
            
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if request.method == 'POST':
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, gt_l('رمز عبور شما با موفقیت تغییر کرد.'))
            return redirect('password_reset_complete')
    else:
        form = CustomSetPasswordForm(user)
    
    return render(request, 'users/password_reset_confirm.html', {'form': form})

def password_reset_complete_view(request):
    return render(request, 'users/password_reset_complete.html')
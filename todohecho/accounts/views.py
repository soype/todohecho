from django.forms.forms import Form
# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import views as auth_views 

from urllib.parse import urlparse, urlunparse

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

UserModel = get_user_model()

from .forms import LoginForm, RegisterForm, ChangeImage
from .models import Account

# Index:  Register line 
#         Login / Logout = Register + 25
#         Change pass = Register + 63


# Register

def view_user(request):
    user = request.user
    form = ChangeImage(instance=user)

    if request.method == 'POST':
        if request.FILES and request.user.profile_image != "logo_1080.png": 
            Account.delete_image(request.user)
        form = ChangeImage(request.POST, request.FILES, instance=user)          
        if form.is_valid:
            form.save()

    context = {'user':user, 'form':form}
    return render(request,'accounts/account.html',context)

def register_view(request,*args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as { user.email }")
    context = {}

    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')  
            account = authenticate(email=email, password=raw_password)
            login(request,account)
            destination = get_redirect_if_exists(request)
            if destination: #if destination != None
              return redirect('tasks:tasks')
            return redirect('tasks:tasks')
        else:
            context['registration_form'] = form


    return render(request, 'accounts/register.html',context)

#Login / Logout    
    
def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request, *args, **kwargs):
    
    context = {}
    
    user = request.user
    
    if user.is_authenticated:
        return redirect('tasks:tasks')
    
    destination = get_redirect_if_exists(request)

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect("tasks:tasks")
                return redirect("tasks:tasks")
        else:
            context['login_form'] = form
    
    return render(request, 'accounts/login.html',context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))
    return redirect
        
# Change/Reset password

def change_password(request):

    return render(request,"password_reset/password_change.html")

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context

class PasswordReset(auth_views.PasswordResetConfirmView):
    template_name = "password_reset/password_reset_confirm.html"
    reset_url_token = "password_reset_confirm"
    
    

    class Meta:
        fields = ['template_name','reset_url_token','title']

class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'password_reset/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'password_reset/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    template_name = 'password_reset/password_reset_form.html'
    title = _('Reiniciar contraseña')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'
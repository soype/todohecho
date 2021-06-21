from todohecho.views import ThanksView
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



#

app_name = "accounts"

urlpatterns = [
    
    #register-login-logout
    path("register/", views.register_view, name="register"),
    path("login/",views.login_view, name="login"),
    path("logout/",views.logout_view, name="logout"),
    path("account/",views.view_user, name="user_detail"),
    
    #password change
    path("password_change/",auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), name="password_change"), 
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), name="password_change_done"),
    #password reset
    path("password_reset/", views.PasswordResetView.as_view(template_name="password_reset/password_reset_form.html"),name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordReset.as_view(template_name="password_reset/password_reset_confirm.html",
                                                                                reset_url_token = "password_reset_confirm",
                                                                                ),name='password_reset_confirm'),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset/password_reset_complete.html"),name="password_reset_complete"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
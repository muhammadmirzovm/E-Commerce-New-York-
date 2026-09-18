from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path("signup/", views.SignUpView.as_view(), name="signup"),
   path("login/", views.CustomLoginView.as_view(), name="login"),
   path("logout/", views.CustomLogoutView.as_view(), name="logout"),
   path("profile/", views.ProfileDetailView.as_view(), name="profile"),
   path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),
   path("password-reset/",views.MyPasswordResetView.as_view(
           template_name="accounts/password_reset_form.html",
           email_template_name="accounts/password_reset_email.txt",
           success_url="/accounts/password-reset/done/",
       ),name="password_reset",),
   path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(
           template_name="accounts/password_reset_done.html",
       ),name="password_reset_done",),
      path("reset/<uidb64>/<token>/",
       auth_views.PasswordResetConfirmView.as_view(
           template_name="accounts/password_reset_confirm.html",
           success_url="/accounts/reset/done/",),
       name="password_reset_confirm",),
   path("reset/done/",
       auth_views.PasswordResetCompleteView.as_view(
           template_name="accounts/password_reset_complete.html",),
       name="password_reset_complete",),  
   path("password-change/",views.MyPasswordChangeView.as_view(
       template_name="accounts/password_change_form.html",
       success_url="done/",),name="password_change",),
    path("password-change/done/",auth_views.PasswordChangeDoneView.as_view(
       template_name="accounts/password_change_done.html",), name="password_change_done",),

]
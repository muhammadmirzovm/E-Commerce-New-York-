from django.urls import path
from . import views

urlpatterns = [
   path("signup/", views.SignUpView.as_view(), name="signup"),
   path("login/", views.CustomLoginView.as_view(), name="login"),
   path("logout/", views.CustomLogoutView.as_view(), name="logout"),
   path("profile/", views.ProfileDetailView.as_view(), name="profile"),
   path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),
]

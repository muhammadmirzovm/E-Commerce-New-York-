from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import SignUpForm, ProfileForm
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views


class SignUpView(CreateView):
   form_class = SignUpForm
   template_name = "accounts/signup.html"
   success_url = reverse_lazy("home")
   def form_valid(self, form):
       response = super().form_valid(form)
       login(self.request, self.object)   
       messages.success(self.request, "Ro‘yxatdan o‘tish muvaffaqiyatli ✅")
       return response
   def form_invalid(self, form):
       messages.error(self.request, "Formada xatolik bor ❌")
       return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def form_valid(self, form):
       messages.success(self.request, "Tizimga kirdingiz ✅")
       return super().form_valid(form)

    def form_invalid(self, form):
       messages.error(self.request, "Login yoki parol xato ❌")
       return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = "home"

    def dispatch(self, request, *args, **kwargs):
       messages.info(request, "Tizimdan chiqdingiz 👋")
       return super().dispatch(request, *args, **kwargs)


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView 
class ProfileDetailView(LoginRequiredMixin, DetailView):
   model = User
   template_name = "accounts/profile_detail.html"
   context_object_name = "profile_user"

   def get_object(self):
       return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("profile")
    def get_object(self):
        return self.request.user
    def form_valid(self, form):
        messages.success(self.request, "Profil yangilandi ✅")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Profilni saqlashda xatolik bor ❌")
        return super().form_invalid(form)

from django.contrib.auth import views as auth_views
class MyPasswordChangeView(auth_views.PasswordChangeView):
   def form_valid(self, form):
       messages.success(self.request, "Parol o‘zgartirildi ✅")
       return super().form_valid(form)


class MyPasswordResetView(auth_views.PasswordResetView):
   def form_valid(self, form):
       messages.info(self.request, "Reset link yuborildi (dev: terminalda) 📩")
       return super().form_valid(form)



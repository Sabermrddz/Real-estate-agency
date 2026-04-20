"""
Views for the accounts app.
Handles user authentication, registration, profile management, and password reset.
"""
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from .forms import RegisterForm, LoginForm, ProfileForm

User = get_user_model()


class RegisterView(CreateView):
    """
    User registration view.
    Creates a new CustomUser account.
    """
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        """
        Save the user and show success message.
        """
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Registration successful! Please log in with your credentials.'
        )
        return response
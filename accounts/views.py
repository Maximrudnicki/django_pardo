from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic.edit import FormView
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.contrib.auth import login

from .forms import UserRegistrationForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('vocab')


class RegisterPage(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('vocab')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('vocab')
        return super(RegisterPage, self).get(*args, **kwargs)


class PasswordChange(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('change_password_done')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/change_password_done.html'
    success_url = reverse_lazy('vocab')

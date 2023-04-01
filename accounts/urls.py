from django.urls import path, include

from accounts.views import (
    CustomLoginView,
    RegisterPage,
    PasswordChange,
    PasswordChangeDone,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('change-password/',
         PasswordChange.as_view(), name='change_password'),
    path('accounts/change-password/done/',
         PasswordChangeDone.as_view(), name='change_password_done'),
]

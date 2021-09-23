
from django.urls import path
from django.contrib.auth import views
from .forms import UserLoginForm
from .views import UserRegisterView ,UserLoginView,EditProfileView,PasswordsChangeView,password_success
urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='register'),
    path('edit_profile/',EditProfileView.as_view(),name='edit_profile'),
    path("password/",PasswordsChangeView.as_view(template_name="registration/change-password.html"),name='change_password'),
    path('password_success',password_success,name="password_success"),

]
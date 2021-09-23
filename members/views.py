from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordChangeView,LoginView
from django.urls import reverse_lazy
from .forms import SignUpForm,UserLoginForm,EditProfilePageForm,PasswordChandingForm
from .models import EmailAuthBackend
from affiliate.models import NewUser
from django.views import generic



class UserRegisterView(CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')
    class Meta:
        model=EmailAuthBackend

class EditProfileView(generic.UpdateView):
    model=NewUser
    form_class=EditProfilePageForm
    template_name = 'registration/edit_profile_page.html'
    success_url = reverse_lazy('home')
    def get_object(self):
        return self.request.user

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChandingForm
    #form_class=PasswordChangeForm
    #success_url=reverse_lazy('home')
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request,"registration/password_success.html",{})




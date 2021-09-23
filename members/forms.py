from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from affiliate.models import NewUser


choise_list=[('adult','adult'),('student','student'),('schooler','schooler')]
class SignUpForm(UserCreationForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model=NewUser
        fields=("email","username",'first_name',"last_name","password1","password2",'status')
    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        self.fields['email'].widget.attrs['class']="form-control"
        self.fields['username'].widget.attrs['class']="form-control"
        self.fields['first_name'].widget.attrs['class'] = "form-control"
        self.fields['last_name'].widget.attrs['class'] = "form-control"
        self.fields['password1'].widget.attrs['class'] = "form-control"
        self.fields['password2'].widget.attrs['class'] = "form-control"
        self.fields['status'].widget.attrs['class'] = "form-control"




class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }))
    class Meta:
        model=NewUser
        fields = ['email', 'password']

class EditProfilePageForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ADULT = 'AD'
    STUDENT = 'SD'
    SCHOOLER = 'SC'

    STATUS_CHOIES = [
        (ADULT, 'Adult'),
        (STUDENT, 'Student'),
        (SCHOOLER, 'Schooler'),

    ]
    status=forms.CharField(max_length=100, widget=forms.Select(attrs={'class': 'form-control'},choices=STATUS_CHOIES))
    class Meta:
        model=NewUser
        fields=('email',"first_name","last_name","username",'status')

class PasswordChandingForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',"type":"password"}))
    new_password1=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control',"type":"password"}))
    new_password2 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control',"type":"password"}))
    class Meta:
        model=User
        fields=("old_password","new_password1","new_password2")




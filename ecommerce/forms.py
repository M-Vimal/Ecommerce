from django import forms
from django.contrib.auth.forms import UserChangeForm,SetPasswordForm
from .models import Customuser,Profile
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'userName'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    role = forms.ChoiceField(
        choices=Customuser.CHOICES,
        widget=forms.Select(attrs={'class': 'form-select w-100'})
    )

    class Meta:
        model = Customuser
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'confirm_password', 'role']


class Update_user_profile(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput)
    last_name = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    password = None
    class Meta:
        model = Customuser
        fields = ['email','username','first_name','last_name']


class Changepassword(SetPasswordForm):
    class Meta:
        model = Customuser
        fields = ['new_password1','new_passsword2']

class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'phone'}),required=False)
    address1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address 1'}),required=False)
    address2 =   forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address 2'}),required=False)
    city = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'city'}),required=False)
    state =  forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'state'}),required=False)
    zipcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'zipcode'}),required=False)
    country = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'country'}),required=False)

    class Meta:
        model = Profile
        fields = ('phone','address1','address2','address2','city','state','zipcode','country')
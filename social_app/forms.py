from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(
        attrs={"class": "bg-gray-200 mb-2 shadow-none  dark:bg-gray-800",'placeholder':'password'}))
    password2 = forms.CharField(label="confirm Password",widget=forms.PasswordInput(
        attrs={"class": "bg-gray-200 mb-2 shadow-none  dark:bg-gray-800",'placeholder':'confirm password'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={"placeholder":"email"}))

    class Meta:
        model = User
        fields = [

            "username",
            "email",
            "password1",
            "password2"
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "bg-gray-200 mb-2 shadow-none  dark:bg-gray-800",'placeholder':'username'}),
           


        }
        help_texts={
            'username':None
        }
        

        # def save(self, commit=True):
        #     user = super(UserCreationForm, self).save(commit=False)
        #     user.email = self.cleaned_data["email"]
        #     if commit:
        #         user.save()
        #     return user
       

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

# class SettingsForm(forms.ModelForm):
#     profile_img=forms.ImageField()
#     bio=forms.CharField(widget=forms.TextInput(attrs={"class":"shadow-none bg-gray-100"}))
#     location=forms.CharField(widget=forms.TextInput(attrs={"class":"shadow-none bg-gray-100"}))
#     class Meta:
#         model=Profile
#         fields=['bio','profile_img','location']
#         widgets = {
#             'profile_img': forms.Textarea(attrs={'rows':1, 'cols':15,
#                                             'autofocus':'autofocus',
#             }),}

       

